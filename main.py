from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, ORJSONResponse, FileResponse, HTMLResponse, JSONResponse
import starlette.status as status
import uvicorn
import os
import sqlite3
#import requests
from apscheduler.schedulers.background import BackgroundScheduler
from db import get_data_one_page, set_data_from_ais, set_data_from_cv, my_task
from __init__ import py_logger #py_logger.info(f"Get index page")

app = FastAPI()
scheduler = BackgroundScheduler()
router = APIRouter()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
timers = 0

@router.get('/to_configurator')
async def to_configurator(request: Request):
    url = "192.168.89.254:9000"
    new_url = f"http://{url}"
    return RedirectResponse(url=new_url, status_code=status.HTTP_302_FOUND)


@router.get('/')
async def root(request:Request):

    #return HTMLResponse(content=html_content, status_code=200)
    return templates.TemplateResponse("archieve.html", {"request": request, "timer":timers})

@app.get("/api/get_recs")
async def get_records(offset: int = 0):
    global timers
    print(timers)
    #print(offset, limit)
    records = get_data_one_page(offset)

    return records

@app.post("/api/set_timer")
async def set_timer(timer):
    global timers
    timers = int(timer)
    
    print(type(timers))
    
    #scheduler.add_job(my_task, 'interval', seconds=3, id='timer')
    #scheduler.remove_all_jobs()
    #scheduler.start()

    try:
        scheduler.pause()
        scheduler.remove_all_jobs()
        scheduler.add_job(my_task, 'interval', args = [timers],  hours=1)
        scheduler.resume()
    except:
        scheduler.add_job(my_task, 'interval', args = [timers], hours=1)
        scheduler.start()
    #scheduler.remove_job('timer')
    
    print(timers, "set timer")

@app.get("/api/get_timer")
async def get_timer():
    global timers
    print(timers)
    return timers

def get_timers():
    global timers
    return timers

@app.post("/api/set_rec_ais")
async def set_rec_ais(data: dict = None):
    set_data_from_ais(data)
    print(data)
    return ORJSONResponse(status_code=200, content={"message":"OK"})

@app.post("/api/set_rec_cv")
async def set_rec_cv(data: dict = None):
    set_data_from_cv(data)
    return ORJSONResponse(status_code=200, content={"message":"OK"})

app.include_router(router)

# @app.on_event("startup")
# def add_job_and_start():
#     scheduler.pause()
#     timers = get_timers()
#     print(timers, "schedule")
#     if timers == 0:
#         scheduler.add_job(my_task, 'interval', seconds=10, coalesce=True, id='timer')
#     elif timers == 1:
#         scheduler.add_job(my_task, 'interval', seconds=30, coalesce=True, id='timer')
#     elif timers == 2:
#         scheduler.add_job(my_task, 'interval', days=14, coalesce=True, id='timer')
#     elif timers == 3:
#         scheduler.add_job(my_task, 'interval', days=30, coalesce=True, id='timer')
#     scheduler.start()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=9030)

