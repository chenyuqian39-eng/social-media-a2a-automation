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


def generate_images_from_prompts(prompts: list[str]) -> list[str]:
    client = get_vertex_client()
    output_files = []

    for i, prompt in enumerate(prompts, start=1):
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
        )

        image_bytes = response.generated_images[0].image.image_bytes

        file_name = f"generated_image_{i}.png"
        with open(file_name, "wb") as f:
            f.write(image_bytes)

        output_files.append(file_name)

    return output_files