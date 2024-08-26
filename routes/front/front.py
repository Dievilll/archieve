from fastapi import APIRouter
from instance.database import get_first_id
from utils.timer import get_timer_api
router = APIRouter(
    prefix='/api',
    tags=['front'],
)

@router.get("/records/get_id_first_rec")
async def get_id_first_record():
    """
    <h1>Возвращает первый идентификатор записей из архива</h1>
    """
    return get_first_id()


@router.get("/db/get_timer")
async def get_timer():
    """
    <h1>Вывод значения таймера</h1>
    """
    return get_timer_api()