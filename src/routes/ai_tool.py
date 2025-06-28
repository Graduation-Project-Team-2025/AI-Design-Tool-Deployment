import os
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
        return JSONResponse(
            status_code=400,
            content={"valid_file": False, "message": signal_eng}
        )

    original_filename, file_id = controller.cache_img(image, project_id)
    image_path = os.path.join(controller.upload_path, project_id, original_filename)
    image_pil = Image.open(image_path).convert("RGB")

    result = controller.generate(image_pil, prompt_arabic, save)
    result_filename, _ = controller.cache_version(result, project_id, file_id)

    base_url = str(request.base_url)
    result_url = base_url + f"image/{project_id}/{result_filename}"

    return JSONResponse(
        status_code=200,
        content={
            "valid_file": True,
            "message": signal_eng,
            "project_id": project_id,
            "file_id": str(file_id),
            "image_url": result_url
        }
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

    image_pil, _ = controller.read_img(project_id, image_id)
    result = controller.regenerate(image_pil, new_prompt_arabic, save)
    result_filename, _ = controller.cache_version(result, project_id, image_id)

    base_url = str(request.base_url)
    result_url = base_url + f"image/{project_id}/{result_filename}"

    return JSONResponse(
        status_code=200,
        content={
            "image_url": result_url,
            "file_id": str(image_id)
        }
    )
