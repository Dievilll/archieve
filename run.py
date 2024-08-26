from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.timer import timers
from settings import tags_metadata
from fastapi.staticfiles import StaticFiles
from __init__ import router
timer_api = timers

app = FastAPI(
    title="VF_config_archive",
    description='Конфигуратор архива событий',
    version='0.0.1',
    openapi_tags=tags_metadata,
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def root(request:Request):
    """
    <h1>Вывод страницы архива</h1>
    """
    global timer_api
    return templates.TemplateResponse("archieve.html", {"request": request, "timer":timer_api})

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=9029)

