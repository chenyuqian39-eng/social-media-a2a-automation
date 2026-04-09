from schemas import ContentBrief, ContentScene, GeneratedPost
from ai_generator import generate_full_post_with_gemini
from imagen_client import generate_images_from_prompts
from veo_client import generate_video_job


def create_viral_caption(topic: str, audience: str, cta: str) -> str:
    return f"Still struggling with {topic}? Save this for later. {cta}"


def generate_trending_audio(platform: str) -> str:
    if platform == "tiktok":
        return "Trending upbeat TikTok lifestyle audio"
    return "Soft aesthetic Rednote background music"


def generate_social_post(brief: ContentBrief) -> GeneratedPost:
    try:
        # 先尝试完整 AI 输出
        post = generate_full_post_with_gemini(brief)

        # AI 成功后，再补 mock Imagen / Veo
        generated_images = generate_images_from_prompts(post.image_prompts)
        video_job = generate_video_job(post.video_prompt)

        post.generated_images = generated_images
        post.video_job = video_job
        return post

    except Exception:
        # fallback: 先把所有字段定义完整
        title = f"{brief.topic.title()} in {brief.duration_seconds} Seconds"
        hook = f"Still struggling with {brief.topic}? Try this."
        caption = f"{brief.topic} tips for {brief.audience}. {brief.cta}"
        hashtags = [
            "#viralcontent",
            "#tiktoktips" if brief.platform == "tiktok" else "#rednotecontent",
            f"#{brief.topic.replace(' ', '')}"
        ]
        suggested_audio_style = generate_trending_audio(brief.platform)

        scenes = [
            ContentScene(
                scene_number=1,
                narration="Hook",
                on_screen_text="Hook",
                visual_direction="Close-up shot",
                duration_seconds=2
            )
        ]

        image_prompts = [
            f"Vertical 9:16 social media image about {brief.topic}, bold hook opening, mobile-first composition",
            f"Vertical 9:16 short-form educational content for {brief.audience}",
            "Vertical 9:16 CTA end card"
        ]

        video_prompt = (
            f"Create an 8-second vertical 9:16 short video about {brief.topic} "
            f"for {brief.audience} with tone {brief.tone} and CTA {brief.cta}."
        )

        generated_images = generate_images_from_prompts(image_prompts)
        video_job = generate_video_job(video_prompt)

        return GeneratedPost(
            title=title,
            hook=hook,
            caption=caption,
            hashtags=hashtags,
            suggested_audio_style=suggested_audio_style,
            scenes=scenes,
            image_prompts=image_prompts,
            video_prompt=video_prompt,
            generated_images=generated_images,
            video_job=video_job
        )