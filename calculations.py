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
		st.write("new")
		#---------------------- creating the extended id -----------------------
		id_ext=str(datetime.date.today().year)
		day_break=str(datetime.date.today().day)
		month_break=str(datetime.date.today().month)
		if(len(month_break)==1):          #adding "0" if month has 1 digit
			id_ext = id_ext + "0"
		id_ext = id_ext + month_break
		if(len(day_break)==1):            #adding "0" if day has 1 digit
			id_ext = id_ext + "0"
		id_ext = id_ext + day_break

		total=0
		cursor.execute("SELECT id_ext FROM breaks WHERE id_ext like '"+id_ext+"%'")    #searching for breaks of the same day as enterd break
		ids=cursor.fetchall()
		for i in range(len(ids)):
			ids[i]=int(ids[i][0])
		if len(ids)==0:
			id_ext=id_ext+"01"
		else:
			id_ext=str(max(ids)+1)
		st.write(id_ext)
		st.write(id_ext[0:4])
		st.write(id_ext[4:6])
		st.write(id_ext[6:8])
		#cursor.execute("INSERT INTO breaks (id_ext, day, month, year) VALUES ("+id_ext+","+str(date_break[0])+","+str(date_break[1])+","+str(date_break[2])+")")
		
	elif status == "add":
		cursor.execute("select max(id_ext) from breaks")
		id_ext=cursor.fetchall()
		st.write(id_ext)
		cursor.execute("select n_coffees from mbr_"+user.upper()+" where id_ext = "+id_ext[0][0])
		st.write("add")
	db.commit()
	db.close()
	return
