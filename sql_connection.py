import sqlite3 as sql


global cur,db

db = sql.connect("gyaanConnect.db")
cur = db.cursor()       

def sqlInsert(cursor_command):

    cursor_command
    db.commit()


def sqlAccess(cursor_command):   
    
    cursor_command
    data = cur.fetchall()
    return data

if __name__ == '__main__':
    pass

