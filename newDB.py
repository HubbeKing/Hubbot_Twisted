import sqlite3

hugs = ["hubbeking",0,0]
line = "Symphony is a cyborg."

conn = sqlite3.connect("hubbot/data/data.db")
c = conn.cursor()

c.execute("CREATE TABLE hugs (nick text, given int, received int)")
c.execute("CREATE TABLE headcanon (canon text)")

c.execute("INSERT INTO hugs VALUES (?, ?, ?)", (hugs[0], hugs[1], hugs[2]))
c.execute("INSERT INTO headcanon VALUES (?)", (line,))

conn.commit()
conn.close()
