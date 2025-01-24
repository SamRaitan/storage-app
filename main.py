import traceback
from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
from pathlib import Path

from ftp import ftp_download_file, ftp_upload_file
from logic.flie_to_image import FileToImg
from logic.image_to_file import ImgToFile

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_extension = str(file.filename).split('.')[1]
        output_image_path = 'temp_file.png'
        print(file.filename)
        ftp_upload_file(FileToImg.process_file_to_image(await file.read(), file.filename))
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {traceback.print_exc()}")
    
    return {"message": "File uploaded successfully", "file_name": file.filename}

@app.get("/download/{file_name}")
async def download_file(file_name: str):
    try:
        file_path = ImgToFile.process_image_to_file(ftp_download_file(file_name))
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {traceback.print_exc()}")


    return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)