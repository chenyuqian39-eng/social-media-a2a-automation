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
- Go inside the week3 files in terminal: cd /User/.../week3
- Python 3.10+

- virtual environment set up
  python3 -m venv venv
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
(checkiing if the configration was set up properly: 
echo $GOOGLE_CLOUD_PROJECT
echo $GOOGLE_CLOUD_LOCATION)
- Set quota project
  gcloud auth application-default set-quota-project YOUR_PROJECT_ID

3. Run the server
  uvicorn main:app --reload 

4. Open the swagger docs and see all the routers which should have:
GET /
GET /agent_card
POST /generate
POST /generate_full_post
POST /create_viral_caption
POST /generate_trending_audio
POST /generate_image_prompts
POST /generate_video_prompt
POST /invoke
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

If successful, the output should include:
title
hook
caption
hashtags
scenes
image_prompts
video_prompt
generated_images
video_job


for POST /create_viral_caption input:
{
  "topic": "cat tips",
  "audience": "students",
  "cta": "Follow for more"
}

should return: 
{
  "caption": "..."
}

for /invoke input:
{
  "skill_name": "generate_full_post",
  "input": {
    "platform": "tiktok",
    "topic": "cat allergy tips",
    "audience": "young pet owners",
    "tone": "friendly",
    "duration_seconds": 8,
    "cta": "Follow for more pet tips"
  }
}
output should be:
{
  "skill_name": "generate_full_post",
  "output": {...}
}
Instead of calling different APIs, we can use a single /invoke endpoint to dynamically execute different skills. This makes the system more suitable for multi-agent architectures.


- Images will be generated and saved locally in week3 folder.
