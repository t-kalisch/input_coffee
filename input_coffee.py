import streamlit as st
import time
from calculations import *

st.set_page_config(page_title="Input Coffee",page_icon="chart_with_upwards_trend",layout="wide")
logged_in = False
header,buf1 = st.columns([1000,0.00001])

@st.cache(suppress_st_warning=True)
def check_login(user, user_pw):
    logged_in = False
    user_data = get_user_data()
    for i in range(len(user_data)):
        if user == user_data[i][0] and user_pw == user_data[i][1]:
            logged_in = True
    return logged_in
        




col1,col2,col3 = st.columns([0.5,1,0.7])
user = col2.text_input(label="", placeholder="Username")
user_pw = col2.text_input(label="", type="password", placeholder="Password")
login = col2.checkbox("Login", help="You are logged in while this checkbox is ticked")
if login:
    logged_in = check_login(user, user_pw)
    if logged_in == True:
        col2.markdown("Logged in as "+user)
    else:
        col2.markdown("Incorrect username or password")
else:
    col2.markdown("Please log in to submit a coffee")
