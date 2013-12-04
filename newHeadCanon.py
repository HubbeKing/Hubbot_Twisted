import sqlite3

line = "Symphony is a cyborg."

conn = sqlite3.connect("data/data.db")
c = conn.cursor()

c.execute("CREATE TABLE headcanon (canon text)")
            
c.execute("INSERT INTO headcanon VALUES (%s)" %line)

conn.commit()
conn.close()