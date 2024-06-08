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
data = {"273334050" :
    {
        "mmsi": 273334050, 
        "status": "<NavigationStatus.Undefined: 15>", 
        "speed": 0.0, 
        "lon": 40.56040, 
        "lat": 64.52050, 
        "course": 360.0, 
        "maneuver": 0,
        "to_port": 0,
        "callsign": "UHDL",
        "destination": "ARHANGELSK",
        "draught":2.5 , 
        "epfd":0,
        "shipClass":83,
        "name":"Kama",
        "imo":0, 
        "key":"hdTQWE_dGER35626"
    }
}

#print (type(data))
json_string = json.dumps(data)
#conn.commit()
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())}"))
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+1}"))
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+2}"))
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+3}"))
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+4}"))
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+5}"))
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "AIS", f"{int(datetime.datetime.now().timestamp())+6}"))
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+7}"))
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+8}"))
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "AIS", f"{int(datetime.datetime.now().timestamp())+9}"))
# cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+10}"))
# #cur.execute("delete from json_data where id IN (SELECT id from json_data order by id desc limit 2)")
# conn.commit()

#cur.execute("SELECT data FROM json_data")


# def repeater(interval, function):
#     Timer(interval, repeater, [interval, function]).start()
#     function()
    
def my_task():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM json_data WHERE id = 190")
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

def get_data_one_page(offset ,id: int):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM json_data WHERE id > {offset}")
    
    result = cur.fetchmany(10)
    cur.close()
    print(result)
    return result
