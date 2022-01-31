import streamlit as st
import datetime
from calculations import *

st.set_page_config(page_title="Input Coffee",page_icon="chart_with_upwards_trend",layout="wide")
logged_in = False
buf1,header2,buf2 = st.columns([0.5,1,0.7])



@st.cache(suppress_st_warning=True)
def check_login(user, user_pw):
    logged_in=[0,0]
    user_data = get_user_data()
    for i in range(len(user_data)):
        if user == user_data[i][0] and user_pw == user_data[i][1]:
            logged_in[0] = 1
            if user_data[i][2] == 1:
                logged_in[1] = 1
    return logged_in

if 'submit' not in st.session_state:
    st.session_state.submit = 0

count=0

col1,col2,col3 = st.columns([0.5,1,0.7])
user = col2.text_input(label="", placeholder="Username")
user_pw = col2.text_input(label="", type="password", placeholder="Password")
login = col2.checkbox("Login", help="You are logged in while this checkbox is ticked")
if login:
    logged_in = check_login(user, user_pw)
    if logged_in[0] == 1:
        header2.markdown("Logged in as "+user)
    else:
        header2.markdown("Incorrect username or password")
else:
    header2.markdown("Please log in to submit a coffee")

if login and logged_in[0] == 1:
    now = datetime.datetime.now()
    break_length = check_breakstatus(now)
    minutes = str(int(break_length.seconds/60))
    seconds = break_length.seconds-(60*int(break_length.seconds/60))
    strseconds = str(seconds)
    if seconds < 10:
        strseconds = "0"+str(seconds)
    if break_length.total_seconds() < 900:
        col2.markdown("A coffee break is under way since "+str(minutes)+":"+strseconds+".")
        col2.button("Update")
        if logged_in[1] == 1:
            name = col2.text_input("Drinker", placeholder = "Username")
            submit_coffee = col2.button("Add coffee to coffee break", help = "A break is under way. Join it by adding a coffee here.", on_click = submit_coffee(user, name, logged_in))
        else:
            submit_coffee = col2.button("Add coffee to coffee break", help = "A break is under way. Join it by adding a coffee here.", on_click = submit_coffee(user, "", logged_in))
    elif break_length.total_seconds() >= 900:
        col2.markdown("No coffee break is currently under way.")
        update = col2.button("Update")
        if logged_in[1] == 1:
            name = col2.text_input("Drinker", placeholder = "Username")
            submit_coffee = col2.button("Start a coffee break", help = "Start a break and add a coffee to your name here.", on_click = submit_coffee(user, name, logged_in))
        else:
            submit_coffee = col2.button("Start a coffee break", help = "Start a break and add a coffee to your name here.", on_click = submit_coffee(user, "", logged_in))
    if submit_coffee:
        st.session_state.submit += 1
st.write(st.session_state.submit)
if update
    st.write(count+1)
