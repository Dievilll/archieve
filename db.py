import sqlite3
import json
import datetime
import threading

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS json_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             data JSON,
             receive TEXT,
             time timestamp);''')
def my_task(timer:int):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    print("my_task", timer)
    time_now = int(datetime.datetime.now().timestamp())
    if timer == 0:
        cur.execute("DELETE FROM json_data WHERE time < ?", (time_now - 86400,))
    elif timer == 1:
        cur.execute("DELETE FROM json_data WHERE time < ?", (time_now - 604800,))
    elif timer == 2:
        cur.execute("DELETE FROM json_data WHERE time < ?", (time_now - 1209600,))
    elif timer == 3:
        cur.execute("DELETE FROM json_data WHERE time < ?", (time_now - 2592000,))
    conn.commit()
    cur.close()
    print("Задача выполнена")

def set_data_from_cv(data: dict):
    cur = conn.cursor()
    json_string = json.dumps(data)
    cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())}"))
    conn.commit()
    cur.close()
    #conn.close()

def set_data_from_ais(data: dict):
    json_string = json.dumps(data)
    cur = conn.cursor()
    cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "AIS", f"{int(datetime.datetime.now().timestamp())}"))
    conn.commit()
    cur.close()
    #conn.close()

def get_fist_id():
    cur = conn.cursor()
    cur.execute("SELECT id FROM json_data ORDER BY id ASC LIMIT 1")
    result = cur.fetchone()
    cur.close()
    return result[0]

def get_data_one_page(offset):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM json_data WHERE id >= {offset}")
    
    result = cur.fetchmany(10)
    cur.close()
    print(result)
    return result
