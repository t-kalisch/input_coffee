import streamlit as st
import datetime
from calculations import *

st.set_page_config(page_title="Input Coffee",page_icon="coffee",layout="wide")

logged_in = False
buf1,header2,buf2 = st.columns([0.5,1,0.7])
header2.title("**:coffee:** Input coffee")

if 'submit' not in st.session_state:
    st.session_state.submit = 0
if 'logged_in' not in st.session_state:
    st.session_state.logged_in=False
if 'attempt' not in st.session_state:
    st.session_state.attempt=False
if 'admin' not in st.session_state:
    st.session_state.admin=False


def check_login(user, user_pw):
    logged_in = False
    user_data = get_user_data()
    for i in range(len(user_data)):
        if user == user_data[i][0] and user_pw == user_data[i][1]:
            logged_in = True
            if user_data[i][2] == 1:
                st.session_state.admin=True
    if logged_in == True:
        st.session_state.logged_in=True
        st.session_state.attempt=False
        st.session_state.submit=0

    else:
        st.session_state.logged_in=False
        st.session_state.attempt=True    

def logout():
        st.session_state.logged_in=False
        st.session_state.attempt=False
        st.session_state.admin=False
        
count=0

col1,col2,col3 = st.columns([0.5,1,0.7])
user = col2.text_input(label="", placeholder="Username", key="username")
user_pw = col2.text_input(label="", type="password", placeholder="Password", key="userpassword")
col1,col2,col3,col4 = st.columns([0.5,0.6,0.4,0.7])
    
if st.session_state.logged_in == True:
    logout = col2.button("Logout", help="Click here to log out", key="logout_button", on_click=logout)
else:
    login = col2.button("Login", help="Click here to log in", key="login_button", on_click=check_login, args=(user, user_pw))
    
col3.checkbox("Remember me", help="Keep me logged in")

            
        
if st.session_state.logged_in == True and st.session_state.attempt == False:
    header2.markdown("Logged in as "+user)
else:
    header2.markdown("Please log in to submit a coffee")




    
    
if st.session_state.attempt == True:
    st.warning("Incorrect username or password")
    
if st.session_state.logged_in == True:
    now = datetime.datetime.now()
    break_length = check_breakstatus(now)
    minutes = str(int(break_length.seconds/60))
    seconds = break_length.seconds-(60*int(break_length.seconds/60))
    strseconds = str(seconds)
    if seconds < 10:
        strseconds = "0"+str(seconds)
        
    if break_length.total_seconds() < 20:
        col2.markdown("A coffee break is under way since "+str(minutes)+":"+strseconds+".")
        update = col2.button("Update", help="Update coffee break status")
        if st.session_state.admin == True:
            name = col2.text_input("Drinker", placeholder = "Username")
            submit_button = col2.button("Add coffee to coffee break", help = "A break is under way. Join it by adding a coffee here.", on_click=submit_coffee, args=(user, name, "add"))
        else:
            submit_button = col2.button("Add coffee to coffee break", help = "A break is under way. Join it by adding a coffee here.", on_click=submit_coffee, args=(user, "", "add"))
    elif break_length.total_seconds() >= 20:
        col2.markdown("No coffee break is currently under way.")
        update = col2.button("Update", help="Update coffee break status")
        if st.session_state.admin == True:
            name = col2.text_input("Drinker", placeholder = "Username")
            submit_button = col2.button("Start a coffee break", help = "Start a break and add a coffee to your name here.", on_click=submit_coffee, args=(user, name, "new"))
        else:
            submit_button = col2.button("Start a coffee break", help = "Start a break and add a coffee to your name here.", on_click=submit_coffee, args=(user, "", "new"))
            
            
st.write(st.session_state.submit)
st.write(st.session_state.logged_in)
st.write(st.session_state.admin)
st.write(st.session_state.attempt)


