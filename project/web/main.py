from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.worker import create_md5_task
from celery.result import AsyncResult
from celery import uuid
import os
import logging

logger = logging.getLogger("web_logger")    

# --- Init FastAPI --- 
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})

@app.post("/upload/")
async def uploadfile(file: UploadFile):
    try:
        task_id = uuid()
        file_path = f"/tmp/appdata/{task_id}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
            # write into DB 
            create_md5_task.apply_async((file_path,), task_id=task_id)
            return JSONResponse({"message": f"task_id: {task_id}"})
    except Exception as e:
        return {"message": e.args}

@app.get("/md5")
def get_md5(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)