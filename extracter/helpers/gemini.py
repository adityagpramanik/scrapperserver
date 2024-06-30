import requests
import os
import json
from dotenv import load_dotenv
from django.http import JsonResponse
from pprint import pprint
import google.generativeai as genai

# load .env
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
GEN_CONFIG = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 2048,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.0-pro",
  generation_config=GEN_CONFIG,
)

def analyseResumeText(resume_text):
    command = "given text is an extract from resume, analyse this text resume and categorize different sections in json format and rate each section out of 10 with reason for rating; text: "
    chat_session = model.start_chat(history=[])

    try:
        response = chat_session.send_message(command + resume_text)
        command = "correct this json and respond only and only in json without any formatting/text/comments: "

        response = chat_session.send_message(command + response.text)
        result = response.text
        result = result.replace('json', '', 1)
        result = result.replace('```', '')
        return json.loads(result)
    except err:
        return JsonResponse({'error': 'Unable to analyse resume text'}, status=403)