from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, ORJSONResponse, FileResponse, HTMLResponse, JSONResponse
import starlette.status as status
import uvicorn
import os
import sqlite3
import datetime
#import requests
from apscheduler.schedulers.background import BackgroundScheduler
from db import get_data_one_page, set_data_from_ais, set_data_from_cv, timer_deletion, get_fist_id, clear_base
from __init__ import py_logger

app = FastAPI()
scheduler = BackgroundScheduler()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
timers = 0

@app.get('/to_configurator')
async def to_configurator(request: Request):
    url = "192.168.89.254:9000"
    new_url = f"http://{url}"
    return RedirectResponse(url=new_url, status_code=status.HTTP_302_FOUND)


@app.get('/')
async def root(request:Request):

    return templates.TemplateResponse("archieve.html", {"request": request, "timer":timers})

@app.get("/api/get_recs")
async def get_records(offset: int = 0):
    global timers
    records = get_data_one_page(offset)

    return records

@app.get("/api/get_id_first_rec")
async def get_records():
    return get_fist_id()

@app.post("/api/delete_base")
async def delete_base():
    return clear_base()

@app.post("/api/set_timer")
async def set_timer(timer):
    global timers
    timers = int(timer)
    py_logger.info(f"|||MAIN --> Установлен новый таймер: {timers}\n0 - 1 день, 1 - 7 дней, 2 - 14 дней, 3 - 30 дней")
    try:
        scheduler.pause()
        scheduler.remove_all_jobs()
        scheduler.add_job(timer_deletion, 'interval', args = [timers],  hours=1)
        scheduler.resume()
    except:
        scheduler.add_job(timer_deletion, 'interval', args = [timers], hours=1)
        scheduler.start()

@app.get("/api/get_timer")
async def get_timer():
    global timers
    return timers

@app.post("/api/set_rec_ais")
async def set_rec_ais(data: dict = None):
    try:
        set_data_from_ais(data)
        py_logger.info(f"|||MAIN --> Новая запись от AIS с временной меткой: {int(datetime.datetime.now().timestamp())}")
    except Exception as e:
        py_logger.error(f"|||MAIN --> Невозможно записать в базу: {e}\nВозможно, data не json")
    return ORJSONResponse(status_code=200, content={"message":"OK"})

@app.post("/api/set_rec_cv")
async def set_rec_cv(data: dict = None):
    try:
        set_data_from_cv(data)
        py_logger.info(f"|||MAIN --> Новая запись от CV с временной меткой {int(datetime.datetime.now().timestamp())}")
    except Exception as e:
        py_logger.error(f"|||MAIN --> Невозможно записать в базу: {e}\nВозможно, data не json")
    return ORJSONResponse(status_code=200, content={"message":"OK"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=9030)

