import json
from fastapi import FastAPI, HTTPException
from schemas import ContentBrief, GeneratedPost, InvokeRequest, InvokeResponse
from generator import generate_social_post, create_viral_caption, generate_trending_audio
from ai_generator import generate_caption_with_gemini

app = FastAPI(title="Content Generator Agent")

# 读取 agent card
with open("agent_card.json", "r", encoding="utf-8") as f:
    AGENT_CARD = json.load(f)


@app.get("/")
def root():
    return {"message": "Content Generator Agent is running"}


@app.get("/agent_card")
def get_agent_card():
    return AGENT_CARD


@app.post("/generate", response_model=GeneratedPost)
def generate(brief: ContentBrief):
    return generate_social_post(brief)


@app.post("/generate_full_post", response_model=GeneratedPost)
def generate_full_post(brief: ContentBrief):
    return generate_social_post(brief)


@app.post("/create_viral_caption")
def create_caption(topic: str, audience: str, cta: str):
    brief = ContentBrief(
        platform="tiktok",
        topic=topic,
        audience=audience,
        tone="friendly",
        duration_seconds=8,
        cta=cta
    )

    try:
        caption = generate_caption_with_gemini(brief)
    except Exception:
        caption = create_viral_caption(topic, audience, cta)

    return {"caption": caption}


@app.post("/generate_trending_audio")
def get_audio(platform: str):
    audio = generate_trending_audio(platform)
    return {"audio_style": audio}


@app.post("/generate_image_prompts")
def get_image_prompts(topic: str, audience: str):
    prompts = [
        f"Vertical 9:16 social media image about {topic}, bold hook opening, mobile-first composition, modern lighting",
        f"Vertical 9:16 educational short-form content for {audience}, clean aesthetic, engaging composition",
        f"Vertical 9:16 polished CTA end card for social media"
    ]
    return {"image_prompts": prompts}


@app.post("/generate_video_prompt")
def get_video_prompt(topic: str, audience: str, tone: str, cta: str):
    prompt = (
        f"Create a vertical 9:16 short video about {topic} for {audience}. "
        f"Tone: {tone}. Include a strong opening hook, fast pacing, subtitle-friendly framing, "
        f"and end with CTA: {cta}."
    )
    return {"video_prompt": prompt}
@app.post("/invoke", response_model=InvokeResponse)
def invoke_agent(request: InvokeRequest):
    skill_name = request.skill_name
    payload = request.input

    if skill_name == "generate_full_post":
        brief = ContentBrief(**payload)
        result = generate_social_post(brief)
        return InvokeResponse(
            skill_name=skill_name,
            output=result.model_dump()
        )

    elif skill_name == "create_viral_caption":
        topic = payload["topic"]
        audience = payload["audience"]
        cta = payload["cta"]

        brief = ContentBrief(
            platform=payload.get("platform", "tiktok"),
            topic=topic,
            audience=audience,
            tone=payload.get("tone", "friendly"),
            duration_seconds=payload.get("duration_seconds", 8),
            cta=cta
        )

        try:
            caption = generate_caption_with_gemini(brief)
        except Exception:
            caption = create_viral_caption(topic, audience, cta)

        return InvokeResponse(
            skill_name=skill_name,
            output={"caption": caption}
        )

    elif skill_name == "generate_trending_audio":
        platform = payload["platform"]
        audio = generate_trending_audio(platform)

        return InvokeResponse(
            skill_name=skill_name,
            output={"audio_style": audio}
        )

    elif skill_name == "generate_image_prompts":
        topic = payload["topic"]
        audience = payload["audience"]

        prompts = [
            f"Vertical 9:16 social media image about {topic}, bold hook opening, mobile-first composition, modern lighting",
            f"Vertical 9:16 educational short-form content for {audience}, clean aesthetic, engaging composition",
            f"Vertical 9:16 polished CTA end card for social media"
        ]

        return InvokeResponse(
            skill_name=skill_name,
            output={"image_prompts": prompts}
        )

    elif skill_name == "generate_video_prompt":
        topic = payload["topic"]
        audience = payload["audience"]
        tone = payload["tone"]
        cta = payload["cta"]

        prompt = (
            f"Create a vertical 9:16 short video about {topic} for {audience}. "
            f"Tone: {tone}. Include a strong opening hook, fast pacing, subtitle-friendly framing, "
            f"and end with CTA: {cta}."
        )

        return InvokeResponse(
            skill_name=skill_name,
            output={"video_prompt": prompt}
        )

    else:
        raise HTTPException(status_code=400, detail=f"Unknown skill: {skill_name}")