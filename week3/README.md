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
1. Environment setup
- Python 3.10+

- virtual environment set up
  python -m venv venv
  For Mac: source venv/bin/activate
  For Win: venv\Scripts\activate

- Install dependencies:
  pip install fastapi uvicorn google-genai pydantic

2. Google Cloud set up
    - gcloud auth application-default login
    - gcloud config set project YOUR_PROJECT_ID
- Set environment variables
  export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
  export GOOGLE_CLOUD_LOCATION="us-central1"

- Set quota project
  gcloud auth application-default set-quota-project YOUR_PROJECT_ID

3. Run the server
  uvicorn main:app --reload 

# Test
http://127.0.0.1:8000/docs

for the POST/generate
one input example is:
"{
  "platform": "tiktok",
  "topic": "cat allergy tips",
  "audience": "young pet owners",
  "tone": "friendly",
  "duration_seconds": 8,
  "cta": "Follow for more pet tips"
}"

- Images will be generated and saved locally in week3 folder.
