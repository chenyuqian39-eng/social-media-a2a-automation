# Project Overview
Standalone Python content generator agent
Generates TikTok / Rednote-style short-form content
Supports skill-based endpoints

I built a standalone Python-based A2A-style content generator agent that generates TikTok and Rednote short-form content on demand.
The system integrates Gemini for content generation, Imagen for image generation, and Veo 3 for video job submission.
The agent exposes its capabilities through an Agent Card and supports skill-based invocation such as generating captions and recommending trending audio.
# Implemented Skills
generate_full_post
create_viral_caption
generate_trending_audio
generate_image_prompts
generate_video_prompt
# Current Integrations
Gemini for AI-generated text
Imagen-ready image prompt generation with mock image outputs
Veo 3-ready 8-second vertical video job generation with mock metadata
# Run
python -m uvicorn main:app --reload
# Test
http://127.0.0.1:8000/docs


