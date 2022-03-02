import mysql.connector as mysql
import streamlit as st
import datetime

#@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
	return mysql.connect(**st.secrets["mysql"])

def db_logout():
	db.close()

def get_user_data():
	db = init_connection()
	cursor = db.cursor(buffered=True)
	cursor.execute("select name, password, admin from members")
	user_data=cursor.fetchall()
	db.close()
	return user_data


def check_breakstatus(now):
	db = init_connection()
	cursor = db.cursor(buffered=True)
	
	cursor.execute("select last_break from update_status")
	last_break = cursor.fetchall()
	duration = now - last_break[0][0]
	#duration.total_seconds()
	return duration

def submit_coffee(user, name, admin):
    active = []
    if admin == True:
        if name == "":
            active.append(user)
        else:
            active.append(name)
    else:
        active.append(user)
    active.append(1)
    #st.session_state.submit = active
    #st.write(st.session_state.submit)
    #st.write(active)
    return
