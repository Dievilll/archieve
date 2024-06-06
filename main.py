from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, ORJSONResponse, FileResponse, HTMLResponse, JSONResponse
import starlette.status as status
import uvicorn
import os
import json
#import requests
from db import get_data_first_page, get_data_one_page
from __init__ import py_logger #py_logger.info(f"Get index page")

app = FastAPI()
router = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@router.get('/to_configurator')
async def to_configurator(request: Request):
    url = "192.168.89.254:9000"
    new_url = f"http://{url}"
    return RedirectResponse(url=new_url, status_code=status.HTTP_302_FOUND)


@router.get('/')
async def root(request:Request):
    #return HTMLResponse(content=html_content, status_code=200)
    return templates.TemplateResponse("archieve.html", {"request": request})

@app.get("/api/get_recs")
async def get_records(offset: int = 0, limit: int = 10):
    print(offset, limit)
    records = get_data_one_page(offset, limit)
    return records
@router.get("/api/next_page")
async def next_page(id: int = 0):

    return JSONResponse(status_code=200, content=get_data_one_page(id, id +10))

@router.get("/api/prev_page")
async def next_page(id: int = 0):

    return JSONResponse(status_code=200, content=get_data_one_page(id, id -10))


app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=9030)
