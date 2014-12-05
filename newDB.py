import os
import sqlite3


def createDB():
    hugs = ["hubbeking",0,0]
    line = "Symphony is a cyborg."

    filename = os.path.join("hubbot", "data", "data.db")
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute("CREATE TABLE hugs (nick text, given int, received int)")
    c.execute("CREATE TABLE headcanon (canon text)")
    c.execute("CREATE TABLE admins (nick text)")
    c.execute("CREATE TABLE ignores (nick text)")
    c.execute("CREATE TABLE aliases (alias text, command text")
    c.execute("CREATE TABLE aliashelp (alias text, help text")
    c.execute("CREATE TABLE lp (id int, message text")
    c.execute("CREATE TABLE mm (id int, message text")
    c.execute("CREATE TABLE pathfinder (id int, message text")
    c.execute("CREATE TABLE welch (id int, message text")

    c.execute("INSERT INTO hugs VALUES (?, ?, ?)", (hugs[0], hugs[1], hugs[2]))
    c.execute("INSERT INTO headcanon VALUES (?)", (line,))

    conn.commit()
    conn.close()
