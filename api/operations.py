from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import starlette.status as status



router = APIRouter(
    prefix='/api',
    tags=['operations'],
)



@router.get('/to_configurator')
async def to_configurator(request: Request):
    """
    <h1>Перенаправляет на страницу конфигуратора</h1>
    """
    url = "192.168.88.250:9000"
    new_url = f"http://{url}"
    return RedirectResponse(url=new_url, status_code=status.HTTP_302_FOUND)