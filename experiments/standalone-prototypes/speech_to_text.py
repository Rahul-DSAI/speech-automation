import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os

def load_whisper_model(model_dir="models/", model_id="openai/whisper-large-v3"):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Construct model save paths
    model_name = model_id.split("/")[-1]
    model_path = os.path.join(model_dir, model_name)
    model_file = os.path.join(model_path, "pytorch_model.bin")  # Model file to check
    processor_dir = os.path.join(model_path, "preprocessor_config.json")  # Processor file to check

    # Download only if necessary
    if not (os.path.exists(model_file) and os.path.exists(processor_dir)):
        print(f"Model files not found. Downloading the model to {model_path}...")
        os.makedirs(model_path, exist_ok=True)

        # Download the model and processor
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

    # Move model to device
    model.to(device)

    # Create a pipeline for speech recognition
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
    # Load Whisper model (either from disk or download it)
    pipe = load_whisper_model(model_dir)
    
    # Perform speech recognition
    result = pipe(audio_file)
    
    # Extract the transcribed text
    return result["text"]
