import sqlite3
connection = sqlite3.connect('database.db')

with open('schema.sql') as fp:
    connection.executescript(fp.read())
cur = connection.cursor()
cur.execute("INSERT INTO todos (descr,isDone) VALUES (?,?)",['Water City',False])
cur.execute("INSERT INTO todos (descr,isDone) VALUES (?,?)",['Spiderbot',False])
cur.execute("INSERT INTO todos (descr,isDone) VALUES (?,?)",['Lava Crystal',False])
cur.execute("INSERT INTO todos (descr,isDone) VALUES (?,?)",['Tip jar',False])
cur.execute("INSERT INTO todos (descr,isDone) VALUES (?,?)",['Cookie Freedom',False])
cur.execute("INSERT INTO todos (descr,isDone) VALUES (?,?)",['Nuclear worm',False])
cur.execute("INSERT INTO todos (descr,isDone) VALUES (?,?)",['Return Conch',False])
cur.execute("INSERT INTO todos (descr,isDone) VALUES (?,?)",['Bean hordes',False])
cur.execute("INSERT INTO todos (descr,isDone) VALUES (?,?)",['Moon germlin',False])
connection.commit()
connection.close()