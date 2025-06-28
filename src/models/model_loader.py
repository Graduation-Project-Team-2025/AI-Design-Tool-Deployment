import os
import torch
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline
from helpers import get_settings

settings = get_settings()
controlnet = ControlNetModel.from_pretrained(settings.CONTROLNET_MODEL)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    settings.BASE_MODEL, controlnet=controlnet
)
pipe.to("cuda" if torch.cuda.is_available() else "cpu")
