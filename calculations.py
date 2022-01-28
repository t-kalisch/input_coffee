import mysql.connector as mysql
import streamlit as st
import datetime

@st.cache
def get_user_data():
	user_data=[['TK', 'akstr!admin2',1],['PB','akstr!admin2',1],['NV',None,None],['DB',None,None],['FLG','baddragon',None],['SHK',None,None],['TB',None,None],['TT',None,None],['RS',None,None]]
	return user_data

def check_breakstatus(now):
	last_break_start = datetime.datetime(2022,1,28,15,20,22)
	duration = now - last_break_start
	#duration.total_seconds()
	return duration
