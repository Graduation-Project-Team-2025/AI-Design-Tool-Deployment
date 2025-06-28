import os
import re
import cv2
from PIL import Image
import base64
import shutil
import uuid
from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseEnum
from utils import (
    save_file, 
    save_temp, 
    delete_file,
    translate_arabic_to_english
)
from models.model_loader import pipe
import numpy as np


class AI_ToolController(BaseController):
    def __init__(self):
        super().__init__()
        self.scale_size = 1048576  # 1 MB in bytes
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.upload_path = os.path.join(base_dir, self.app_settings.UPLOAD_FILES_PATH)

    def generate(self, image: Image.Image, prompt_arabic: str, save: bool = False):
        prompt_en = translate_arabic_to_english(prompt_arabic)
        output = pipe(prompt=prompt_en, image=image).images[0]

        if save:
            os.makedirs("outputs", exist_ok=True)
            filename = f"outputs/output_{uuid.uuid4().hex[:8]}.png"
            output.save(filename)

        return output

    def regenerate(self, image: Image.Image, prompt_arabic: str, save: bool = False):
        return self.generate(image, prompt_arabic, save)

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return (
                False,
                ResponseEnum.FILE_TYPE_NOT_SUPPORTED_ENG.value,
                ResponseEnum.FILE_TYPE_NOT_SUPPORTED_AR.value
            )

        if file.size > self.app_settings.FILE_ALLOWED_SIZE * self.scale_size:
            return (
                False,
                ResponseEnum.FILE_SIZE_EXCEEDED_ENG.value,
                ResponseEnum.FILE_SIZE_EXCEEDED_AR.value
            )
        
        return (
            True,
            ResponseEnum.FILE_UPLOADED_SUCCESSFULLY_ENG.value,
            ResponseEnum.FILE_UPLOADED_SUCCESSFULLY_AR.value
        )

    def validate_project_id(self, project_id):
        project_path = os.path.join(self.upload_path, project_id)
        if os.path.exists(project_path):
            return (
                True,
                ResponseEnum.PROJECT_FOUND_SUCCESSFULLY_ENG.value,
                ResponseEnum.PROJECT_FOUND_SUCCESSFULLY_AR.value
            )
        else:
            return (
                False,
                ResponseEnum.PROJECT_DOES_NOT_EXIST_ENG.value,
                ResponseEnum.PROJECT_DOES_NOT_EXIST_AR.value
            )

    def validate_file_id(self, file_id, project_id):
        project_path = os.path.join(self.upload_path, project_id)
        filenames = os.listdir(project_path)
        pattern_img = r"^(?P<file_id>.+)-IMG-ORG\.(?:png|jpg|jpeg)$"
        file_ids = []
        for fname in filenames:
            match = re.match(pattern_img, fname, re.IGNORECASE)
            if match:
                file_ids.append(match.group("file_id"))
        if file_id in file_ids:
            return (
                True,
                ResponseEnum.FILE_FOUND_SUCCESSFULLY_ENG.value,
                ResponseEnum.FILE_FOUND_SUCCESSFULLY_AR.value
            )
        else:
            return (
                False,
                ResponseEnum.FILE_DOES_NOT_EXIST_ENG.value,
                ResponseEnum.FILE_DOES_NOT_EXIST_AR.value
            )

    def file_exists(self, project_id, filename):
        project_path = os.path.join(self.upload_path, project_id)
        file_path = os.path.join(project_path, filename)
        if os.path.exists(file_path):
            return (
                True,
                ResponseEnum.FILE_FOUND_SUCCESSFULLY_ENG.value,
                ResponseEnum.FILE_FOUND_SUCCESSFULLY_AR.value,
                file_path
            )
        else:
            return (
                False,
                ResponseEnum.FILE_DOES_NOT_EXIST_ENG.value,
                ResponseEnum.FILE_DOES_NOT_EXIST_AR.value,
                ""
            )
    def cache_img(self, file: UploadFile, project_id: str):
        filename , file_id = save_file(file, project_id=project_id,
                                        upload_dir=self.app_settings.UPLOAD_FILES_PATH)
        return filename , file_id 

    def cache_version(self, file, project_id: str, file_id: str):
        if isinstance(file, Image.Image):
            file = np.array(file)  # Convert to NumPy before passing
        filename, file_id = save_file(
            file, project_id,
            file_id=file_id,
            upload_dir=self.app_settings.UPLOAD_FILES_PATH
        )
        return filename, file_id
    

