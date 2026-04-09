
import time
import json
import time
from google import genai
from schemas import ContentBrief, GeneratedPost
client = genai.Client()


def generate_caption_with_gemini(brief: ContentBrief) -> str:
    prompt = f"""
    Create exactly ONE short viral social media caption.

    Platform: {brief.platform}
    Topic: {brief.topic}
    Audience: {brief.audience}
    Tone: {brief.tone}
    CTA: {brief.cta}

    Rules:
    - Return only one final caption
    - Do not give multiple options
    - Do not use headings like Option 1
    - Do not use markdown
    - Keep it concise and social-media ready
    - Add 3 to 5 hashtags at the end
    """

    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception:
            time.sleep(1)

    raise Exception("Gemini failed after retries")

def generate_post_fields_with_gemini(brief: ContentBrief) -> dict:
    prompt = f"""
    Generate short-form social media content fields for this brief.

    Platform: {brief.platform}
    Topic: {brief.topic}
    Audience: {brief.audience}
    Tone: {brief.tone}
    Duration: {brief.duration_seconds} seconds
    CTA: {brief.cta}

    Return in this exact format:
    TITLE: ...
    HOOK: ...
    CAPTION: ...
    HASHTAGS: #tag1, #tag2, #tag3
    """

    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            text = response.text.strip()

            result = {
                "title": "",
                "hook": "",
                "caption": "",
                "hashtags": []
            }

            for line in text.splitlines():
                if line.startswith("TITLE:"):
                    result["title"] = line.replace("TITLE:", "").strip()
                elif line.startswith("HOOK:"):
                    result["hook"] = line.replace("HOOK:", "").strip()
                elif line.startswith("CAPTION:"):
                    result["caption"] = line.replace("CAPTION:", "").strip()
                elif line.startswith("HASHTAGS:"):
                    tags = line.replace("HASHTAGS:", "").strip()
                    result["hashtags"] = [tag.strip() for tag in tags.split(",") if tag.strip()]

            return result
        except Exception:
            time.sleep(1)

    return {}


def generate_full_post_with_gemini(brief: ContentBrief) -> GeneratedPost:
    prompt = f"""
You are a short-form social media content generator.

Generate a short-form social media content package in VALID JSON ONLY.

The content is for:
- Platform: {brief.platform}
- Topic: {brief.topic}
- Audience: {brief.audience}
- Tone: {brief.tone}
- Duration: {brief.duration_seconds} seconds
- CTA: {brief.cta}

Return ONLY JSON in exactly this structure:
{{
  "title": "...",
  "hook": "...",
  "caption": "...",
  "hashtags": ["#tag1", "#tag2", "#tag3"],
  "suggested_audio_style": "...",
  "scenes": [
    {{
      "scene_number": 1,
      "narration": "...",
      "on_screen_text": "...",
      "visual_direction": "...",
      "duration_seconds": 2
    }},
    {{
      "scene_number": 2,
      "narration": "...",
      "on_screen_text": "...",
      "visual_direction": "...",
      "duration_seconds": 2
    }},
    {{
      "scene_number": 3,
      "narration": "...",
      "on_screen_text": "...",
      "visual_direction": "...",
      "duration_seconds": 2
    }},
    {{
      "scene_number": 4,
      "narration": "...",
      "on_screen_text": "...",
      "visual_direction": "...",
      "duration_seconds": 2
    }}
  ],
  "image_prompts": ["...", "...", "..."],
  "video_prompt": "..."
}}

Strict rules:
1. Return ONLY valid JSON
2. Do NOT wrap the JSON in markdown
3. Do NOT include explanation text
4. Create EXACTLY 4 scenes
5. Total scene duration must equal {brief.duration_seconds} seconds
6. Scene 1 must be a strong hook
7. Scene 2 must explain the problem or context
8. Scene 3 must provide a useful tip or solution
9. Scene 4 must end with a clear CTA
10. Keep the language short, punchy, and social-media friendly
11. Make it suitable for vertical 9:16 short-form video
12. The caption must sound natural and not repeat words awkwardly
13. Include 3 to 5 relevant hashtags
14. Make image prompts visually descriptive for Imagen
15. Make the video prompt suitable for Veo 3 short video generation

Important:
- The output must be production-ready
- The content should feel like TikTok/Rednote content
- Do not leave any field empty
"""

    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            text = response.text.strip()
            data = json.loads(text)
            return GeneratedPost.model_validate(data)

        except Exception:
            time.sleep(1)

    raise Exception("Gemini full post generation failed")