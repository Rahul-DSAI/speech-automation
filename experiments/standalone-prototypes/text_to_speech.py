import torch
from transformers import AutoProcessor, AutoModelForTextToWaveform
from scipy.io.wavfile import write as write_wav
from playsound import playsound

# Load the processor and model
processor = AutoProcessor.from_pretrained("suno/bark")
model = AutoModelForTextToWaveform.from_pretrained("suno/bark")

def text_to_speech_bark(text, output_file="speech.wav", voice_preset=None):
    # Prepare input for the Bark model
    inputs = processor(text, return_tensors="pt", voice_preset=voice_preset)

    # Generate audio waveform
    with torch.no_grad():
        audio_array = model.generate(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"]).cpu().numpy().squeeze()

    # Save the generated audio as a WAV file
    write_wav(output_file, 24000, audio_array)  # Bark uses 24kHz sample rate
    print(f"Speech saved to {output_file}")

    # Play the generated speech using playsound
    playsound(output_file)
