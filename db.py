import sqlite3
import json
import datetime
conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS json_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             data JSON)''')
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

cur.execute("INSERT INTO json_data (data) VALUES (?)", (json_string,))
#cur.execute("delete from json_data where id IN (SELECT id from json_data order by id desc limit 2)")
conn.commit()

cur.execute("SELECT data FROM json_data")
def get_data():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM json_data")
    result = cur.fetchall()
    #a = json.loads(result[1][0])
    print(result[0][1])
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
