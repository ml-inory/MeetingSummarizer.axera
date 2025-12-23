from typing import Annotated, Optional
from fastapi import APIRouter, File, Form, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.models.asr.asr_abc import ASR
from app.models.asr.factory import ASRFactory


router = APIRouter(
    prefix="/v1/audio",
    tags=["audio"],
    responses={404: {"description": "Not found"}},
)


class Item(BaseModel):
    text: str


responses = {
    400: {"description": "Illegal parameters"},
    404: {"description": "Item not found"},
    504: {"description": "Internal server error"},
    200: {
        "description": "Transcription result",
        "content": {"application/json": {"example": {"text": "Let there be light"}}},
    },
}


@router.get("/transcriptions/debug")
async def debug():
    return {
        "text": "Imagine the wildest idea that you've ever had, and you're curious about how it might scale to something that's a 100, a 1,000 times bigger. This is a place where you can get to do that.",
    }


@router.post("/transcriptions", response_model=Item, responses=responses)
async def transcriptions(
    request: Request,
    file: Annotated[bytes, File()],
    model: Optional[str] = Form("sensevoice"),
    language: Optional[str] = Form("auto"),
    stream: Optional[bool] = Form(False),
):
    # Check parameters
    asr_model: ASR = request.app.state.ml_model.get("transcriptions", None)
    if asr_model is None:
        return JSONResponse(
            content="Transcription model is not init",
            status_code=504,
        )

    if model not in ASRFactory.supported_models:
        return JSONResponse(
            content=f"Not support model: {model}, currently support: {ASRFactory.supported_models}",
            status_code=400,
        )
    
    if language not in asr_model.supported_languages():
        return JSONResponse(
            content=f"Not support language: {language}, currently support: {asr_model.supported_languages()}",
            status_code=400,
        )
    
    # # Use await request.form() to parse the body
    # form_data = await request.form()

    # # form_data is a FormData object (like a dict)
    # username = form_data.get("username")

    # # Files are retrieved as UploadFile objects
    # file: UploadFile = form_data.get("file")

    # if file:
    #     # Access file attributes
    #     filename = file.filename
    #     content_type = file.content_type

    #     # Read file content asynchronously
    #     # For large files, consider writing to disk in chunks instead of reading all into memory
    #     contents = await file.read()

    #     # Process the file content (e.g., save it, analyze it)
    #     # Remember to seek to the beginning if you need to read it again later
    #     await file.seek(0)

    #     return {
    #         "username": username,
    #         "filename": filename,
    #         "content_type": content_type,
    #         "file_size": len(contents)
    #     }

    
    return {"text": asr_model.supported_languages()}
