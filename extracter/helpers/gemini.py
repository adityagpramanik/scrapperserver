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
    current_folder_path = os.path.dirname(os.path.abspath(__file__))
    input_folder_path = os.path.join(current_folder_path, 'llmrefs')
    history = [
      {
        "role": "user",
        "parts": [open(os.path.join(input_folder_path, "input-01.txt")).read()],
      },
      {
        "role": "user",
        "parts": [open(os.path.join(input_folder_path, "input-02.txt")).read()],
      },
      {
        "role": "model",
        "parts": [open(os.path.join(input_folder_path, "output-01.txt")).read()],
      },
    ]
    chat_session = model.start_chat(history=history)

    try:
        response = chat_session.send_message(resume_text)
        result = response.text
        result = result.replace('json', '', 1)
        result = result.replace('```', '')

        return json.loads(result)
    except:
        return JsonResponse({'error': 'Unable to analyse resume text'}, status=403)