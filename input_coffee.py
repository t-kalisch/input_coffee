import streamlit as st
import time
from calculations import *

logged_in = False
header = st.columns([1])

@st.cache
def check_login(user, user_pw)
    user_data = get_user_data()
    for i in range(len(user_data)):
        if user == user_data[i][0] and user_pw == user_data[i][1]:
            logged_in = True
        else:
            header.warning("Incorrect username or password.")


st.set_page_config(page_title="Input Coffee",page_icon="chart_with_upwards_trend",layout="wide")


col1,col2,col3 = st.columns([0.5,1,0.7])
user = col1.text_input(label="", placeholder="Username")
user_pw = col1.text_input(label="", type="password", placeholder="Password")
login = col1.checkbox("Login", help="You are logged in while this checkbox is ticked")
if login:
  check_login(user, user_pw)
