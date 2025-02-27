import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

# Read API key from environment variable
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Split
def split_into_sentences(text):
    """Splits text into sentences using regex."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())  # Split on ., !, ?
    return [s.strip() for s in sentences if s.strip()]  # Remove empty parts

# Transcribing function
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )

    content = transcription.text
    sentences = split_into_sentences(content)
    pages = []
    current_page = 1

    while sentences:
        page_sentences = sentences[:5]  # Take up to max_sentences_per_page
        sentences = sentences[5:]  # Remove used sentences
        
        pages.append({
            "page_number": current_page,
            "content": " ".join(page_sentences)  # Merge sentences back into a page
        })
        current_page += 1  # Increment page number

    return pages

# Main
audio_file = "mp3/audio1.mp3"
json_data = transcribe_audio(audio_file)

# Save to JSON file
with open("json/transcriptions2.json", "w", encoding="utf-8") as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

print("Transcriptions saved to transcriptions.json")
