from instance.database import get_data_one_page, set_data_from_ais, set_data_from_cv

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse



router = APIRouter(
    prefix='/api',
    tags=['records'],
)


@router.get("/records/get_recs")
async def get_recs(offset: int = 0):
    """
    <h1>Вывод записей из архива на страницу</h1>

    <h2>Параметы:</h2>\n
        - offset: смещение(int)

    <h2>Возврат:</h2>\n
        - массив в виде: 
            [(id:1, {data:...}, receive:..., time:...), id:2, {data:...}, receive:..., time:...), ...]
    """
    return get_data_one_page(offset)


@router.post("/records/set_rec_ais")
async def set_rec_ais(data:dict):
    """
    <h1>Новая запись от AIS</h1>

    <h2>Параметры:</h2>\n
        - data: 
            {"data":"..."}
    
    <h2>Возврат:</h2>\n
        - {
            "message":"...", 
            "data":{
            "...": "..."
            }
          }
    """
    set_data_from_ais(data)
    return ORJSONResponse(status_code=200, content={"message":"OK", "data":data})

@router.post("/records/set_rec_cv")
async def set_rec_cv(data: dict):
    """
    <h1>Новая запись от CV</h1>

    <h2>Параметры:</h2>\n
        - data: 
            {"data":"..."}
    
    <h2>Возврат:</h2>\n
        - {
            "message":"...", 
            "data":{
            "...": "..."
            }
          }
    """
    set_data_from_cv(data)
    return ORJSONResponse(status_code=200, content={"message":"OK", "data":data})