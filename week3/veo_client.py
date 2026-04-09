import os
from google import genai


def get_vertex_client():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT is not set. Please export GOOGLE_CLOUD_PROJECT first."
        )

    return genai.Client(
        vertexai=True,
        project=project_id,
        location=location,
    )


def generate_video_job(video_prompt: str) -> dict:
    client = get_vertex_client()

    operation = client.models.generate_videos(
        model="veo-3.0-generate-001",
        prompt=video_prompt,
        config={
            "duration_seconds": 8,
            "aspect_ratio": "9:16"
        }
    )

    return {
        "job_id": getattr(operation, "name", "unknown_operation"),
        "status": "submitted",
        "provider": "veo-3",
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
        "prompt": video_prompt
    }