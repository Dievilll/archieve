from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, ORJSONResponse, FileResponse, HTMLResponse, JSONResponse
import starlette.status as status
import uvicorn
import os
import sqlite3
import json
#import requests
from db import get_data_first_page, get_data_one_page
from __init__ import py_logger #py_logger.info(f"Get index page")
app = FastAPI()

templates = Jinja2Templates(directory="templates")
def get_records_from_database(offset, id: int):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM json_data WHERE id >= {id}")
    result = cur.fetchmany(10)
    #a = json.loads(result[1][0])
    #print(result[0][1])
    #print (b,"dsadsda")
    conn.close()
    print("res", result[-1][0])
    #result = json.loads(result)
    return result


@app.get('/')
async def root(request:Request):
    #return HTMLResponse(content=html_content, status_code=200)
    global id
    return templates.TemplateResponse(
        "dsa.html", context={"request": request}
)

@app.get("/api/next_records")
async def get_next_records(offset: int = 0):
    # Здесь должен быть ваш код для получения следующих 10 записей из базы данных
    # Используйте offset для определения, какие записи нужно получить
    records = get_records_from_database(offset, offset +10)
    return JSONResponse(content=records)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)