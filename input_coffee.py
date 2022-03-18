import streamlit as st
import datetime
from calculations import *
import pandas as pd
import extra_streamlit_components as stx

st.set_page_config(page_title="Input Coffee",page_icon="coffee",layout="wide")

@st.cache(allow_output_mutation=True, suppress_st_warning = True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookie_manager.get_all()

if 'submit' not in st.session_state:
    st.session_state.submit = 0
if 'logged_in' not in st.session_state:
    st.session_state.logged_in=False
if 'user' not in st.session_state:
    st.session_state.user=None
if 'attempt' not in st.session_state:
    st.session_state.attempt=False
if 'admin' not in st.session_state:
    st.session_state.admin=False

if cookie_manager.get(cookie="logged_in") == "true":
    st.session_state.logged_in="true"
    st.session_state.user = cookie_manager.get(cookie="user")
    st.session_state.admin=cookie_manager.get(cookie="status")


#logged_in=st.session_state.logged_in


buf1,header2,buf2 = st.columns([0.5,1,0.7])
header2.title("**:coffee:** Input coffee")

        
count=0

col1,col2,col3 = st.columns([0.5,1,0.7])
user = col2.text_input(label="", placeholder="Username", key="username")
user_pw = col2.text_input(label="", type="password", placeholder="Password", key="userpassword")
col1,col2,col3,col4 = st.columns([0.5,0.6,0.4,0.7])

remember_me = col3.checkbox("Remember me", help="Keep me logged in (uses cookies)")

def check_login(user, user_pw):
    logged_in = False
    user_data = get_user_data()
    for i in range(len(user_data)):
        if user == user_data[i][0] and user_pw == user_data[i][1]:
            logged_in = True
            st.session_state.user=user.upper()
            if user_data[i][2] == 1:
                st.session_state.admin=True
    if logged_in == True:
        st.session_state.logged_in=True
        st.session_state.attempt=False
        st.session_state.submit=0
        #if remember_me:
        #    cookie_manager.set("logged_in", st.session_state.logged_in, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logged_in_true")
        #    cookie_manager.set("user", st.session_state.user, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logged_in_user")
        #    cookie_manager.set("status", st.session_state.admin, expires_at=datetime.datetime(year=2030, month=1, day=1), key="admin_status")
        #else:
        #    cookie_manager.set("logged_in", False, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logout")
        #    cookie_manager.set("status", None, expires_at=datetime.datetime(year=2030, month=1, day=1), key="del_admin_status")
        #    cookie_manager.set("user", None, expires_at=datetime.datetime(year=2030, month=1, day=1), key="logged_in_user") 
    else:
        st.session_state.logged_in=False
        st.session_state.attempt=True    

def logout():
        st.session_state.logged_in=False
        st.session_state.attempt=False
        st.session_state.admin=False
        st.session_state.user=None



if st.session_state.logged_in == True:
    logout = col2.button("Logout", help="Click here to log out", key="logout_button", on_click=logout)
else:
    login = col2.button("Login", help="Click here to log in", key="login_button", on_click=check_login, args=(user, user_pw))
    





        
if st.session_state.logged_in == True and st.session_state.attempt == False:
    header2.markdown("Logged in as "+st.session_state.user)
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
        
    if break_length.total_seconds() <= 785:                                                 #average break length is 13:05.0171 aka 785 seconds
        buf1,middle,buf2 = st.columns([0.5,1,0.7]) 
        middle.markdown("A coffee break is under way since "+str(minutes)+":"+strseconds+". (total length: 13:05)")
        col1,col2,col3,col4 = st.columns([0.5,0.6,0.4,0.7])
        update = col2.button("Update", help="Update coffee break status")
        if st.session_state.admin == True:
            name = col2.text_input("Drinker", placeholder = st.session_state.user)
            submit_button = col2.button("Add coffee to coffee break", help = "A break is under way. Join it by adding a coffee here.", on_click=submit_coffee, args=(st.session_state.user, name))
            col2.write("-" * 34)
            col1,col2,col3,col4,col5 = st.columns([0.5,0.3,0.3,0.4,0.7])
            current = cur_break()
            col2.write("Persons")
            col2.write(current[0][0])
            col3.write("Coffees")
            col3.write(current[0][1])
            col1,col2,col3,col4 = st.columns([0.5,0.6,0.4,0.7])
            del_person = col2.text_input("Delete coffee for person", placeholder = "Username")
            del_coffee = col2.button("Delete coffee from current break", on_click=delete_coffee, args=(del_person,""))
        else:
            submit_button = col2.button("Add coffee to coffee break", help = "A break is under way. Join it by adding a coffee here.", on_click=submit_coffee, args=(st.session_state.user, ""))
    elif break_length.total_seconds() > 785:                                                #average break length is 13:05.0171 aka 785 seconds
        col2.markdown("No coffee break is currently under way.")
        update = col2.button("Update", help="Update coffee break status")
        if st.session_state.admin == True:
            name = col2.text_input("Drinker", placeholder = st.session_state.user)
            submit_button = col2.button("Start a coffee break", help = "Start a break and add a coffee to your name here.", on_click=submit_coffee, args=(st.session_state.user, name))
        else:
            submit_button = col2.button("Start a coffee break", help = "Start a break and add a coffee to your name here.", on_click=submit_coffee, args=(st.session_state.user, ""))
            


