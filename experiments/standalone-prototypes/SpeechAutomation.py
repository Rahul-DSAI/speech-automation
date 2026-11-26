import sounddevice as sd 
import numpy as np
import soundfile as sf
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os
import google.generativeai as genai
from gtts import gTTS
from playsound import playsound

# Function to record audio
def record_audio(duration=5, fs=16000):
    print("Recording... Please speak into the microphone.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.float32)
    sd.wait()  # Wait until recording is finished
    print("Recording complete!")
    return np.squeeze(audio)

# Save recorded audio to a file
def save_audio(audio, filename="temp_audio.wav", fs=16000):
    sf.write(filename, audio, fs)
    print(f"Audio saved to {filename}")

def load_whisper_model(model_dir="models/", model_id="openai/whisper-large-v3"):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_name = model_id.split("/")[-1]
    model_path = os.path.join(model_dir, model_name)
    model_file = os.path.join(model_path, "pytorch_model.bin")
    processor_dir = os.path.join(model_path, "preprocessor_config.json")

    if not (os.path.exists(model_file) and os.path.exists(processor_dir)):
        print(f"Model files not found. Downloading the model to {model_path}...")
        os.makedirs(model_path, exist_ok=True)

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, cache_dir=model_path, low_cpu_mem_usage=True, use_safetensors=True
        )
        processor = AutoProcessor.from_pretrained(model_id, cache_dir=model_path)
    else:
        print(f"Model files found at {model_path}. Loading from disk...")
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_path, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        processor = AutoProcessor.from_pretrained(model_path)

    model.to(device)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
    )

    return pipe

def speech_to_text(audio_file, model_dir="models/"):
    pipe = load_whisper_model(model_dir)
    result = pipe(audio_file)
    return result["text"]

class GoogleGeminiAPI:
    def __init__(self, api_key, model_name="models/gemini-1.0-pro-latest"):
        self.api_key = api_key
        self.model_name = model_name
        self.model = None

    def gcp_config(self):
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_model(self):
        try:
            self.gcp_config()
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            print(f"An error occurred: {e}")

    def generate_text(self, prompt, text):
        try:
            if not self.model:
                self.load_model()
            response = self.model.generate_content(prompt + text)
            return response.text
        except Exception as e:
            print(f"generate_text:: {e}")
            return None

def correct_grammar(api_key, text):
    prompt = '''
        You are a highly knowledgeable language teacher with in-depth expertise in multiple languages, including their grammar, pronunciation, and vocabulary. Your role is to teach language learners how to speak fluently and accurately in any language they choose...
        '''
    gemini_api = GoogleGeminiAPI(api_key)
    return gemini_api.generate_text(prompt, text)

def text_to_speech(text, output_file="speech.mp3", lang="en"):
    # Initialize gTTS object
    tts = gTTS(text=text, lang=lang)

    # Save the speech to an MP3 file
    tts.save(output_file)
    print(f"Speech saved to {output_file}")

    # Play the saved audio file
    playsound(output_file)

def main():
    # Step 1: Record audio
    audio = record_audio(duration=5)
    audio_file = "temp_audio.wav"
    save_audio(audio, audio_file)

    # Step 2: Convert recorded audio to text
    print("Converting speech to text...")
    transcribed_text = speech_to_text(audio_file, model_dir="models/")
    print("Transcribed Text:", transcribed_text)

    # Step 3: Correct grammar and pronunciation
    api_key = "REDACTED_GOOGLE_API_KEY"  # Replace with your actual API key
    print("Correcting grammar and pronunciation...")
    corrected_text = correct_grammar(api_key, transcribed_text)
    print("Corrected Text:", corrected_text)

    # Step 4: Convert corrected text to speech using gTTS
    print("Converting corrected text to speech...")
    output_audio_file = "final_output.mp3"
    text_to_speech(corrected_text, output_file=output_audio_file)
    print(f"Final speech saved to {output_audio_file}")

if __name__ == "__main__":
    main()
