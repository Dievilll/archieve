import sqlite3
import json
import datetime
import threading
from __init__ import py_logger

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS json_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             data JSON,
             receive TEXT,
             time timestamp);''')


def no_copy_code(time_now:int, delation:int):
    try:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT data FROM json_data WHERE time < ?", (time_now - delation,))
        result = cur.fetchall()
        py_logger.info(f"Удалена(-ы) запись(-и) {result}")
        cur.execute("DELETE FROM json_data WHERE time < ?", (time_now - delation,))
        conn.commit()
        cur.close()
    except Exception as e:
        py_logger.error(f"Ошибка удаления базы -->{e}")
def timer_deletion(timer:int):

    #print("my_task", timer)
    time_now = int(datetime.datetime.now().timestamp())
    if timer == 0:
        no_copy_code(time_now, 86400)
    elif timer == 1:
        no_copy_code(time_now, 604800)
    elif timer == 2:
        no_copy_code(time_now, 1209600)
    elif timer == 3:
        no_copy_code(time_now, 2592000)

    #print("Задача выполнена")

def set_data_from_cv(data: dict):
    try:
        cur = conn.cursor()
        json_string = json.dumps(data)
        py_logger.info(f"|||DB --> Новая запись от CV: {data}")
        cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())}"))
        conn.commit()
        cur.close()
    except Exception as e:
        py_logger.error(f"|||DB --> Невозможно записать в базу: {e}\nВозможно, data не json")
    #conn.close()

def set_data_from_ais(data: dict):
    try:
        json_string = json.dumps(data)
        cur = conn.cursor()
        py_logger.info(f"|||DB --> Новая запись от AIS: {data}")
        cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "AIS", f"{int(datetime.datetime.now().timestamp())}"))
        conn.commit()
        cur.close()
    except Exception as e:
        py_logger.error(f"|||DB --> Невозможно записать в базу: {e}\nВозможно, data не json")
    #conn.close()

def get_fist_id():
    cur = conn.cursor()
    cur.execute("SELECT id FROM json_data ORDER BY id ASC LIMIT 1")
    result = cur.fetchone()
    cur.close()
    try:
        return result[0]
    except Exception as e:
        py_logger.error("|||DB --> Невозможно взять элементы таблицы: БАЗА ДАННЫХ ПУСТА \n {e}")

def get_data_one_page(offset):
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT * FROM json_data WHERE id >= {offset}")
        
        result = cur.fetchmany(10)
        cur.close()
    except Exception as e:
        py_logger.error("|||DB --> Невозможно получить данные: БАЗА ДАННЫХ ПУСТА \n {e}")
    #print(result)
    return result

def clear_base():
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS json_data")
    cur.execute('''CREATE TABLE IF NOT EXISTS json_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             data JSON,
             receive TEXT,
             time timestamp);''')
    print("OK")
    conn.commit()
    cur.close()
    return True