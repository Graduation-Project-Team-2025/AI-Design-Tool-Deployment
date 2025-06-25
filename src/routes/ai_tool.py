from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import os
import uuid
import io
from controllers.AI_ToolController import AI_ToolController
from controllers.AI_ToolController import validate_uploaded_file

router = APIRouter(
    prefix="/designer",
    tags=["designer"]
)

@router.post("/generate")
async def generate_endpoint(
    image: UploadFile = File(...),
    prompt_arabic: str = Form(...),
    save: bool = Form(False)
):
    validate_uploaded_file(image)
    image_pil = Image.open(image.file).convert("RGB")

    image_id = uuid.uuid4().hex[:10]
    input_path = os.path.join(os.getenv("UPLOAD_FILES_PATH"), f"{image_id}.png")
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    image_pil.save(input_path)

    result = generate(image_pil, prompt_arabic, save)
    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png", headers={"X-Image-ID": image_id})


@router.post("/regenerate")
async def regenerate_endpoint(
    image_id: str = Form(...),
    new_prompt_arabic: str = Form(...),
    save: bool = Form(False)
):
    file_path = os.path.join(os.getenv("UPLOAD_FILES_PATH"), f"{image_id}.png")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image ID not found")

    image_pil = Image.open(file_path).convert("RGB")
    result = generate(image_pil, new_prompt_arabic, save)
    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")