import sqlite3
import json
import datetime
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

data['time'] = f"{int(datetime.datetime.now().timestamp())}"
print (type(data))
json_string = json.dumps(data)

cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())}"))
cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+1}"))
cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+2}"))
cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+3}"))
cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+4}"))
cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+5}"))
cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "AIS", f"{int(datetime.datetime.now().timestamp())+6}"))
cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+7}"))
cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+8}"))
cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "AIS", f"{int(datetime.datetime.now().timestamp())+9}"))
cur.execute("INSERT INTO json_data (data, receive, time) VALUES (?, ?, ?)", (json_string, "CV", f"{int(datetime.datetime.now().timestamp())+10}"))
#cur.execute("delete from json_data where id IN (SELECT id from json_data order by id desc limit 2)")
conn.commit()

cur.execute("SELECT data FROM json_data")
def get_data_first_page(offset ,id: int):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM json_data WHERE id > {id}")
    result = cur.fetcmany(10)
    print(result)
    #a = json.loads(result[1][0])
    #print(result[0][1])
    #print (b,"dsadsda")
    conn.close()
    #result = json.loads(result)
    return result

def get_data_one_page(offset ,id: int):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM json_data WHERE id > {offset}")
    result = cur.fetchmany(10)
    print(result)
    #a = json.loads(result[1][0])
    #print(result[0][1])
    #print (b,"dsadsda")
    conn.close()
    #result = json.loads(result)
    return result
#result = cur.fetchone()
#print(result)
#json_string = result[0]
#conn.close()
#json_data = json.loads(json_string)

#print(json_data)
