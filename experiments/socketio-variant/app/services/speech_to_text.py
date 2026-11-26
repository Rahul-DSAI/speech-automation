import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_api_key = your_openai_api_key
client = OpenAI(api_key=openai_api_key)

async def openai_speech_to_text(audio_file: str) -> str:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=open(audio_file, "rb")
    )
    return transcription.text