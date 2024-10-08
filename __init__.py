import logging
from logging.handlers import RotatingFileHandler
import os
from fastapi import APIRouter
from api import operations, db, records
from routes.front import front
router = APIRouter()
router.include_router(db.router)
router.include_router(operations.router)
router.include_router(records.router)
router.include_router(front.router)
#router.include_router(reports.router)

os.makedirs("logger", exist_ok=True)
py_logger = logging.getLogger('archieve')
py_logger.setLevel(logging.INFO)
# настройка обработчика и форматировщика в соответствии с нашими нуждами
py_handler = RotatingFileHandler(f"logger/{'archieve'}.log", mode='a', encoding= 'utf-8', maxBytes=200*1024*1024,backupCount=5)
py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику 
py_handler.setFormatter(py_formatter)
# добавление обработчика к логгеру
if py_logger.hasHandlers():
    py_logger.handlers.clear()
py_logger.addHandler(py_handler)
