import sqlite3

hugs = ["hubbeking",0,0]

conn = sqlite3.connect("data/data.db")
c = conn.cursor()

c.execute("CREATE TABLE hugs (nick text, given int, received int)")

c.execute("INSERT INTO hugs VALUES (%s, %s, %s)" %(hugs[0], hugs[1], hugs[2]))
