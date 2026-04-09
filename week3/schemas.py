from pydantic import BaseModel, Field
from typing import Literal
from typing import Any


class ContentBrief(BaseModel):
    platform: Literal["tiktok", "rednote"]
    topic: str
    audience: str
    tone: str
    duration_seconds: int = Field(default=8, ge=5, le=60)
    cta: str


class ContentScene(BaseModel):
    scene_number: int
    narration: str
    on_screen_text: str
    visual_direction: str
    duration_seconds: int


class GeneratedPost(BaseModel):
    title: str
    hook: str
    caption: str
    hashtags: list[str]
    suggested_audio_style: str
    scenes: list[ContentScene]
    image_prompts: list[str]
    video_prompt: str
    generated_images: list[str] | None = None
    video_job: dict | None = None


class InvokeRequest(BaseModel):
    skill_name: str
    input: dict[str, Any]


class InvokeResponse(BaseModel):
    skill_name: str
    output: dict[str, Any]