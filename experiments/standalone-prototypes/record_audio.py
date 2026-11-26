import sounddevice as sd
import numpy as np
import soundfile as sf

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
