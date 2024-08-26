from fastapi import Request, WebSocket
from fastapi.responses import RedirectResponse, ORJSONResponse, HTMLResponse
import starlette.status as status
from instance.database import clear_base
#from service.__init__ import templates
from utils.logger_db import py_logger
from utils.timer import set_timer_api
#from models.models import Event
#from service.__init__ import websocket_thread
from fastapi import APIRouter


#app.mount("/static", StaticFiles(directory="static"), name="static")
router = APIRouter(
    prefix='/api',
    tags=['db'],
)

@router.post("/db/delete_base")
async def delete_base():
    """
    <h1>ПОЛНАЯ ОЧИСТКА БАЗЫ ДАННЫХ</h1>
    """
    clear_base()
    return ORJSONResponse(status_code=200, content={"message": "OK"})

@router.post("/db/set_timer")
async def set_timer(timer):
        """
        <h1>Установка нового таймера удаления записей</h1>
        
        <h2>Параметры:</h2>\n
             - timer: (0 - 1 день, 1 - 7 дней, 2 - 14 дней, 3 - 30 дней)
        
        <h2>Возврат:</h2>\n
             - Статус и значение таймера
        """
        if set_timer_api(int(timer)):
            return ORJSONResponse(status_code=200, content={"message": "OK", "timer": timer})
        else:
             py_logger.error("|||API --> Значение таймера неверно. Возможные значения: 0, 1, 2, 3")
             return ORJSONResponse(status_code=403, content={"message": "Значение таймера неверно. Возможные значения: 0, 1, 2, 3"})
    #except Exception as e:
        



