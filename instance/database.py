#import psycopg2 as pg
import json
import datetime
from utils.logger_db import py_logger
from sqlalchemy import Column, Integer, String, JSON, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Records(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    data = Column(JSON, default='{}')
    receive = Column(String, default='')
    time = Column(Integer, default=0)


engine = create_engine("postgresql://postgres:postgres@127.0.0.1:5432/archive")
Base.metadata.create_all(engine)

new_session = sessionmaker(engine, expire_on_commit=False)


def no_copy_code(time_now:int, delation:int):
    try:
        session = new_session()
        records = [rec.data for rec in session.query(Records).filter(Records.time < time_now - delation)]
        #if len(records) < 1:
        #    pass
        #else:
        #lst = []
        #for item in records:
        #    lst.append(item.data)
        #print (lst)
        session.query(Records).filter(Records.time < time_now - delation).delete()
        session.commit()
        session.close()
        py_logger.info(f"Удалена(-ы) запись(-и) {records}")
    except Exception as e:
        py_logger.error(f"Ошибка удаления базы -->{e}")

def timer_deletion(timer:int):
    time_now = int(datetime.datetime.now().timestamp())
    if timer == 0:
        no_copy_code(time_now, 3600)
    elif timer == 1:
        no_copy_code(time_now, 604800)
    elif timer == 2:
        no_copy_code(time_now, 1209600)
    elif timer == 3:
        no_copy_code(time_now, 2592000)

def set_data_from_cv(data: dict):
    try:
        session = new_session()
        json_string = json.dumps(data)
        py_logger.info(f"|||DB --> Новая запись от CV: {data}")
        rec = Records()
        rec.data, rec.receive, rec.time = json_string, "CV", int(datetime.datetime.now().timestamp())
        session.add(rec)
        session.commit()
        session.close()
    except Exception as e:
        py_logger.error(f"|||DB --> Невозможно записать в базу: {e}\nВозможно, data не json")

def set_data_from_ais(data: dict):
    try:
        session = new_session()
        json_string = json.dumps(data)
        py_logger.info(f"|||DB --> Новая запись от CV: {data}")
        rec = Records()
        rec.data, rec.receive, rec.time = json_string, "AIS", int(datetime.datetime.now().timestamp())
        session.add(rec)
        session.commit()
        session.close()
    except Exception as e:
        py_logger.error(f"|||DB --> Невозможно записать в базу: {e}\nВозможно, data не json")

def get_first_id():
    try:
        session = new_session()
        rec = session.query(Records.id).first()[0]
        session.close()
        print(rec, "first_id")
        return rec
    except Exception as e:
        py_logger.error(f"|||DB --> Невозможно взять элементы таблицы: БАЗА ДАННЫХ ПУСТА \n {e}")

def get_data_one_page(offset):
    try:
        session = new_session()
        recs = session.query(Records).order_by(Records.id).where(Records.id >= offset).limit(10)
        lst = []
        for item in recs:
            lst.append(item)
        session.close()
        return lst
    except Exception as e:
        py_logger.error(f"|||DB --> Невозможно получить данные: БАЗА ДАННЫХ ПУСТА \n {e}")
            

def clear_base():
    Records.__table__.drop(engine)
    Records.__table__.create(engine)
    py_logger.info(f"|||DB --> БАЗА ДАННЫХ ОЧИЩЕНА")
    print("OK")
    return True