import os
import uuid
from PIL import Image
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from controllers import AI_ToolController

router = APIRouter(
    prefix="/designer",
    tags=["designer"]
)

@router.post("/{project_id}/generate")
async def generate_endpoint(
    request: Request,
    project_id: str,
    image: UploadFile = File(...),
    prompt_arabic: str = Form(...),
    save: bool = Form(False)
):
    controller = AI_ToolController()

    is_valid, signal_eng, _ = controller.validate_uploaded_file(image)
    if not is_valid:
        raise HTTPException(status_code=400, detail=signal_eng)

    image_pil = Image.open(image.file).convert("RGB")
    image_id = uuid.uuid4().hex[:10]

    upload_dir = os.getenv("UPLOAD_FILES_PATH", "./uploads")
    input_path = os.path.join(upload_dir, project_id)
    os.makedirs(input_path, exist_ok=True)

    original_path = os.path.join(input_path, f"{image_id}.png")
    image_pil.save(original_path)

    result = controller.generate(image_pil, prompt_arabic, save)
    result_path = os.path.join(input_path, f"{image_id}_result.png")
    result.save(result_path)

    base_url = str(request.base_url)
    result_url = base_url + f"image/{project_id}/{image_id}_result.png"

    return JSONResponse(
        status_code=200,
        content={"image_url": result_url}
    )

@router.post("/{project_id}/regenerate")
async def regenerate_endpoint(
    request: Request,
    project_id: str,
    image_id: str = Form(...),
    new_prompt_arabic: str = Form(...),
    save: bool = Form(False)
):
    controller = AI_ToolController()

    upload_dir = os.getenv("UPLOAD_FILES_PATH", "./uploads")
    input_path = os.path.join(upload_dir, project_id)
    image_path = os.path.join(input_path, f"{image_id}.png")

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Original image not found")

    image_pil = Image.open(image_path).convert("RGB")

    result = controller.regenerate(image_pil, new_prompt_arabic, save)
    result_path = os.path.join(input_path, f"{image_id}_regenerated.png")
    result.save(result_path)

    # Build URL
    base_url = str(request.base_url)
    result_url = base_url + f"image/{project_id}/{image_id}_regenerated.png"

    return JSONResponse(
        status_code=200,
        content={"image_url": result_url}
    )
