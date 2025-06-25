import os
from helpers import get_settings
from utils import download_models
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline
from transformers import pipeline

if __name__ == '__main__':
    settings = get_settings()
    model_ids = [
        settings.CONTROLNET_MODEL,
        settings.BASE_MODEL,
        settings.TRANSLATION_MODEL
    ]
    base_dir = os.path.dirname(__file__)
    save_path = os.path.join(base_dir, settings.MODELS_WEIGHTS_PATH)

    model_paths = download_models(model_ids, save_path)

    controlnet = ControlNetModel.from_pretrained(model_paths[0])
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        model_paths[1], controlnet=controlnet
    )
    translator = pipeline("translation", model=model_paths[2])

    print("All models downloaded and loaded successfully.")