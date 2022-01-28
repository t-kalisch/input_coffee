import mysql.connector as mysql
import streamlit as st

@st.cache
def get_user_data():
	user_data=[['TK', 'akstr!admin2',1],['PB','akstr!admin2',1],['NV',None,None],['DB',None,None],['FLG','baddragon',None],['SHK',None,None],['TB',None,None],['TT',None,None],['RS',None,None]]
	return user_data
