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

# Function to play back recorded audio
def play_audio(audio, fs=16000):
    print("Playing back recorded audio...")
    sd.play(audio, samplerate=fs)
    sd.wait()  # Wait until playback is finished
    print("Playback complete!")

# Record audio from the microphone (5 seconds)
audio = record_audio(duration=5)

# Save recorded audio to a temporary file (optional)
sf.write("temp_audio.wav", audio, 16000)

