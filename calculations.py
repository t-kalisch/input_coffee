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


def submit_coffee(user, name):
	db = init_connection()
	cursor = db.cursor(buffered=True)
	break_length = check_breakstatus(datetime.datetime.now())
	if break_length.total_seconds() > 785:                                                 #average break length is 13:05.0171 aka 785 seconds
		cursor.execute("update update_status set last_break = current_timestamp()")
		db.commit()
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
		cursor.execute("INSERT INTO breaks (id_ext, day, month, year) VALUES ("+id_ext+","+str(int(id_ext[6:8]))+","+str(int(id_ext[4:6]))+","+str(int(id_ext[0:4]))+")")
		cursor.execute("insert into break_sizes (id_ext, size) values ("+id_ext+", 1)")
		if name == "":
			cursor.execute("insert into mbr_"+user.upper()+" (id_ext, n_coffees) values (%s, %s)", (id_ext, 1))
			cursor.execute("insert into drinkers (id_ext, persons, coffees) values (%s, %s, %s)", (id_ext, user.upper(), 1))
		else:
			cursor.execute("insert into mbr_"+name.upper()+" (id_ext, n_coffees) values (%s, %s)", (id_ext, 1))
			cursor.execute("insert into drinkers (id_ext, persons, coffees) values (%s, %s, %s)", (id_ext, name.upper(), 1))
		st.success("Your 1. coffee for this break has been saved!")
		
	elif break_length.total_seconds() <= 785:                                                #average break length is 13:05.0171 aka 785 seconds
		cursor.execute("select max(id_ext) from breaks")
		id_ext=cursor.fetchall()[0][0]
		
		cursor.execute("select persons, coffees from drinkers where id_ext = "+id_ext)
		drinkers_old = cursor.fetchall()[0]
		if name == "":
			cursor.execute("select count(n_coffees) from mbr_"+user.upper()+" where id_ext = "+id_ext)
			tmp=cursor.fetchall()[0][0]
			
			if tmp == 0:
				cursor.execute("insert into mbr_"+user.upper()+" (id_ext, n_coffees) values (%s, %s)", (id_ext, 1))
				persons = drinkers_old[0] + "-" + user.upper()
				coffees = drinkers_old[1] + "-1"
				cursor.execute("update drinkers set persons = '"+persons+"' where id_ext = "+id_ext)
				cursor.execute("update drinkers set coffees = '"+coffees+"' where id_ext = "+id_ext)
				cursor.execute("select size from break_sizes where id_ext = "+id_ext)
				size=cursor.fetchall()
				cursor.execute("update break_sizes set size = "+str(size[0][0]+1)+" where id_ext = "+id_ext)
				coffees_mbr = 1
			else:
				cursor.execute("select n_coffees from mbr_"+user.upper()+" where id_ext = "+id_ext)
				coffees_mbr = cursor.fetchall()[0][0]+1
				cursor.execute("update mbr_"+user.upper()+" set n_coffees = "+str(coffees_mbr)+" where id_ext = "+id_ext)
				persons = drinkers_old[0].split("-")
				coffees = drinkers_old[1].split("-")
				coffees_new = ""
				for i in range(len(persons)):
					if user.upper() == persons[i]:
						coffees[i] = str(int(coffees[i]) + 1)
					coffees_new = coffees_new + str(coffees[i])
					if i < len(persons)-1:
						coffees_new = coffees_new + "-"
				#cursor.execute("update drinkers set persons = "+persons+" where id_ext = "+id_ext)
				cursor.execute("update drinkers set coffees = '"+coffees_new+"' where id_ext = "+id_ext)
		else:
			cursor.execute("select count(n_coffees) from mbr_"+name.upper()+" where id_ext = "+id_ext)
			tmp=cursor.fetchall()[0][0]
			if tmp == 0:
				cursor.execute("insert into mbr_"+name.upper()+" (id_ext, n_coffees) values (%s, %s)", (id_ext, 1))
				persons = drinkers_old[0] + "-" + name.upper()
				coffees = drinkers_old[1] + "-1"
				cursor.execute("update drinkers set persons = '"+persons+"' where id_ext = "+id_ext)
				cursor.execute("update drinkers set coffees = '"+coffees+"' where id_ext = "+id_ext)
				cursor.execute("select size from break_sizes where id_ext = "+id_ext)
				size=cursor.fetchall()
				cursor.execute("update break_sizes set size = "+str(size[0][0]+1)+" where id_ext = "+id_ext)
				coffees_mbr = 1
			else:
				cursor.execute("select n_coffees from mbr_"+name.upper()+" where id_ext = "+id_ext)
				coffees_mbr = cursor.fetchall()[0][0]+1
				cursor.execute("update mbr_"+name.upper()+" set n_coffees = "+str(coffees_mbr)+" where id_ext = "+id_ext)
				persons = drinkers_old[0].split("-")
				coffees = drinkers_old[1].split("-")
				coffees_new = ""
				for i in range(len(persons)):
					if name.upper() == persons[i]:
						coffees[i] = str(int(coffees[i]) + 1)
					coffees_new = coffees_new + str(coffees[i])
					if i < len(persons)-1:
						coffees_new = coffees_new + "-"
				#cursor.execute("update drinkers set persons = "+persons+" where id_ext = "+id_ext)
				cursor.execute("update drinkers set coffees = '"+coffees_new+"' where id_ext = "+id_ext)
		st.success("Your "+str(coffees_mbr)+". coffee for this break has been saved!")
	db.commit()
	db.close()
	return


def delete_coffee(name, test):
	db = init_connection()
	cursor = db.cursor(buffered=True)
	
	cursor.execute("select id_ext, persons, coffees from drinkers ORDER BY id DESC LIMIT 1")
	tmp=cursor.fetchall()
	id_ext = tmp[0][0]
	persons = tmp[0][1].split("-")
	coffees = tmp[0][2].split("-")

	for i in range(len(persons)):
		if persons[i] == name.upper():
			if int(coffees[i]) > 0:
				coffees[i] = int(coffees[i]) - 1
				cursor.execute("update mbr_"+name.upper()+" set n_coffees = "+str(coffees[i])+" where id_ext = '"+id_ext+"'")
				st.success("A coffee for "+persons[i]+" has been deleted. They now have "+str(coffees[i])+" coffees in the current break.")
		if coffees[i] == 0:
			cursor.execute("delete from mbr_"+name.upper()+" where id_ext = '"+id_ext+"'")

	persons_new = ""
	coffees_new = ""
	for i in range(len(persons)):
		if coffees[i] == 0:
			pass
		else:
			if persons_new == "":
				persons_new += persons[i]
				coffees_new += str(coffees[i])
			else:
				persons_new = persons_new + "-" + persons[i]
				coffees_new = coffees_new + "-" + str(coffees[i])
	if persons_new == "":
		cursor.execute("DELETE FROM breaks WHERE id_ext='"+id_ext+"'")
		cursor.execute("update update_status set last_break = timestamp(subdate(current_date, 1))")
		st.success("No drinker remains in the current break, therefore the break has been deleted.")
	else:
		cursor.execute("update drinkers set persons = '"+persons_new+"' where id_ext = '"+id_ext+"'")
		cursor.execute("update drinkers set coffees = '"+coffees_new+"' where id_ext = '"+id_ext+"'")
	db.commit()
	db.close()

def cur_break():
	db = init_connection()
	cursor = db.cursor(buffered=True)
	cursor.execute("select persons, coffees from drinkers ORDER BY id DESC LIMIT 1")
	current = cursor.fetchall()
	return current
