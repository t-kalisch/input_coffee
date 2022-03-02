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
	
	db.close()
	return duration


def submit_coffee(user, name, status):
	db = init_connection()
	cursor = db.cursor(buffered=True)
	
	if status == "new":
		cursor.execute("update update_status set last_break = current_timestamp()")
		st.write("added")
	elif status == "add":
		st.write("öafdj")
		cursor.execute("select max(id_ext) from breaks")
		id_ext=cursor.fetchall()
		cursor.execute("select n_coffees from mbr_"+user.upper()+" where id_ext = "+id_ext[0][0])
		
	
	db.commit()
	db.close()
	return
