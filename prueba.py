import os
import google.generativeai as genai
from dotenv import load_dotenv


# Cargar las variables del archivo .env
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

for model in genai.list_models():
  if 'generateContent' in model.supported_generation_methods:
    print(model.name)