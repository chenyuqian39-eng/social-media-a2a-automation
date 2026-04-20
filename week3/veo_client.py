import os
import time
import subprocess

from google import genai
from google.genai.types import GenerateVideosConfig


def get_vertex_client():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is not set.")

    return genai.Client(
        vertexai=True,
        project=project_id,
        location=location,
    )


def generate_video_job(video_prompt: str) -> dict:
    client = get_vertex_client()

    output_gcs_uri = os.getenv("VEO_OUTPUT_GCS_URI")
    if not output_gcs_uri:
        raise ValueError("VEO_OUTPUT_GCS_URI is not set.")

    operation = client.models.generate_videos(
        model="veo-3.1-generate-001",
        prompt=video_prompt,
        config=GenerateVideosConfig(
            aspect_ratio="9:16",
            duration_seconds=8,
            output_gcs_uri=output_gcs_uri,
        ),
    )

    print("[INFO] Veo operation submitted:", operation)

    # 轮询直到完成
    while not operation.done:
        print("[INFO] Waiting for Veo video generation to finish...")
        time.sleep(15)
        operation = client.operations.get(operation)
        print("[INFO] Current operation state:", operation)

    # 如果 operation 本身失败
    if operation.error is not None:
        print(f"[ERROR] Veo operation failed: {operation.error}")
        return {
            "job_id": getattr(operation, "name", "unknown_operation"),
            "status": "failed",
            "provider": "veo-3.1",
            "duration_seconds": 8,
            "aspect_ratio": "9:16",
            "prompt": video_prompt,
            "video_uri": None,
            "video_file": None,
        }

    # 取结果并自动下载到本地
    try:
        video_uri = operation.result.generated_videos[0].video.uri

        # 创建本地输出目录
        local_dir = "outputs"
        os.makedirs(local_dir, exist_ok=True)

        # 取文件名
        filename = os.path.basename(video_uri.rstrip("/"))
        local_path = os.path.join(local_dir, filename)

        # 从 GCS 下载到本地
        subprocess.run(
            ["gsutil", "cp", video_uri, local_path],
            check=True
        )

        print(f"[INFO] Video downloaded to: {local_path}")

        return {
            "job_id": getattr(operation, "name", "unknown_operation"),
            "status": "completed",
            "provider": "veo-3.1",
            "duration_seconds": 8,
            "aspect_ratio": "9:16",
            "prompt": video_prompt,
            "video_uri": video_uri,
            "video_file": local_path,
        }

    except Exception as e:
        print(f"[ERROR] Failed to read or download Veo result: {e}")
        return {
            "job_id": getattr(operation, "name", "unknown_operation"),
            "status": "failed",
            "provider": "veo-3.1",
            "duration_seconds": 8,
            "aspect_ratio": "9:16",
            "prompt": video_prompt,
            "video_uri": None,
            "video_file": None,
        }
