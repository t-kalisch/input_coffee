import streamlit as st
import datetime
from calculations import *

st.set_page_config(page_title="Input Coffee",page_icon="chart_with_upwards_trend",layout="wide")
logged_in = False
buf1,header2,buf2 = st.columns([0.5,1,0.7])

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
        header2.markdown("Logged in as "+user)
    else:
        header2.markdown("Incorrect username or password")
else:
    header2.markdown("Please log in to submit a coffee")

if login and logged_in == True:
    now = datetime.datetime.now()
    break_length = check_breakstatus(now)
    st.write(check_breakstatus(now).total_seconds())
    if break_length.total_seconds() < 900:
        st.markdown("A coffee break is under way since "+str(break_length.seconds//3600)+":"+str(break_length.seconds//60)%60+":")#+str(break_length.seconds))
        submit_coffee = col2.button("Add coffee to coffee break", help = "A break is under way. Join it by adding a coffee here.")
    elif break_length.total_seconds() >= 900:
        submit_coffee = col2.button("Start a coffee break", help = "Start a break and add a coffee to your name here.")
