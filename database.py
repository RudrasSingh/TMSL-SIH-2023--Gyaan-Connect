import sqlite3
from flask import g

def connect_to_database():
    # Get the database connection 
    if 'db' not in g:
        g.db = sqlite3.connect('gyaanConnect.db')

def get_database():
    # Get the database connection 
    if 'db' not in g:
        connect_to_database()
    return g.db

def close_connection():
    # Close the database connection
    db = g.pop('db', None)
    if db is not None:
        db.close()

#table-1 : dashboard

def create_dashboard(email, name, address, p_score, course):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO dashboard (email, name, address, p_score, course) 
                      VALUES (?, ?, ?, ?, ?)''', (email, name, address, p_score, course))
    db.commit()

def fetch_dashboards():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM dashboard''')
    rows = cursor.fetchall()
    return rows

def update_dashboard(email, name, address, p_score, course):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE dashboard SET name=?, address=?, p_score=?, course=? WHERE email=?''', 
                   (name, address, p_score, course, email))
    db.commit()

def delete_dashboard(email):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM dashboard WHERE email=?''', (email,))
    db.commit()

#table-2 : Gyx credits

def create_gyx(time, email, credits):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO gyx (time, email, credits) 
                      VALUES (?, ?, ?)''', (time, email, credits))
    db.commit()

def fetch_gyx():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM gyx''')
    rows = cursor.fetchall()
    return rows

def update_gyx(time, email, credits):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE gyx SET time=?, credits=? WHERE email=?''', 
                   (time, credits, email))
    db.commit()

def delete_gyx(email):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM gyx WHERE email=?''', (email,))
    db.commit()

#table-3 : user_login

"""def create_login(email, name, password, ayatech):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO login (email, name, password, ayatech) 
                      VALUES (?, ?, ?, ?)''', (email, name, password, ayatech))
    db.commit()

def fetch_logins():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM login''')
    rows = cursor.fetchall()
    return rows

def update_login(email, name, password, ayatech):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE login SET name=?, password=?, ayatech=? WHERE email=?''', 
                   (name, password, ayatech, email))
    db.commit()
  
def delete_login(email):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM login WHERE email=?''', (email,))
    db.commit()"""


#table-4 : personal details

def create_pers_det(email, first_name, last_name, college, gender, location, phone, dob, course, topic, level, pf_pic):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO pers_det (email, first_name, last_name, college, gender, location, phone, dob, course, topic, level, pf_pic) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (email, first_name, last_name, college, gender, location, phone, dob, course, topic, level, pf_pic))
    db.commit()

def fetch_pers_det(email):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM pers_det where email=?''',(email))
    rows = cursor.fetchall()
    return rows

def update_pers_det(email, first_name, last_name, college, gender, location, phone, dob, course, topic, level, pf_pic):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE pers_det SET first_name=?, last_name=?, college=?, gender=?, location=?, phone=?, dob=?, course=?, topic=?, level=?, pf_pic=? WHERE email=?''', 
                   (first_name, last_name, college, gender, location, phone, dob, course, topic, level, pf_pic, email))
    db.commit()

def delete_pers_det(email):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM pers_det WHERE email=?''', (email,))
    db.commit()


#table-5 : Teacher_login

def create_tech_login(email, profile_pic, f_name, l_name, skill, git, fb, twitter, insta, org, exp, gender, location, phone, dob, lang):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO tech_login (email, profile_pic, f_name, l_name, skill, git, fb, twitter, insta, org, exp, gender, location, phone, dob, lang) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (email, profile_pic, f_name, l_name, skill, git, fb, twitter, insta, org, exp, gender, location, phone, dob, lang))
    db.commit()

def fetch_tech_login():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM tech_login''')
    rows = cursor.fetchall()
    return rows

def update_tech_login(email, profile_pic, f_name, l_name, skill, git, fb, twitter, insta, org, exp, gender, location, phone, dob, lang):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE tech_login SET profile_pic=?, f_name=?, l_name=?, skill=?, git=?, fb=?, twitter=?, insta=?, org=?, exp=?, gender=?, location=?, phone=?, dob=?, lang=? WHERE email=?''', 
                   (profile_pic, f_name, l_name, skill, git, fb, twitter, insta, org, exp, gender, location, phone, dob, lang, email))
    db.commit()

def delete_tech_login(email):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM tech_login WHERE email=?''', (email,))
    db.commit()


# Additional functions:

def fetch_table_names():
    db = get_database()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return tables
