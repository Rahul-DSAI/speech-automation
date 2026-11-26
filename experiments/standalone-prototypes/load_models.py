import os
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

def load_whisper_model(model_dir="models/"):
    model_name = "openai/whisper-large-v3"

    # Create model directory if it doesn't exist
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_path = os.path.join(model_dir, model_name)

    # Check if the model is already downloaded, if not download it
    if not os.path.exists(model_path):
        print(f"Downloading the Whisper model '{model_name}' to {model_dir}...")
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_name, 
            cache_dir=model_dir,  # Specify the directory to save the model
            use_safetensors=True  # Ensure you're using the correct format
        )
        processor = AutoProcessor.from_pretrained(model_name, cache_dir=model_dir)
        print(f"Model '{model_name}' downloaded and saved in {model_dir}.")
    else:
        print(f"Loading the Whisper model from {model_dir}...")
        model = AutoModelForSpeechSeq2Seq.from_pretrained(model_path, use_safetensors=True)
        processor = AutoProcessor.from_pretrained(model_path)
    
    return model, processor
