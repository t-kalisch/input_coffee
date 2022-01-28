import streamlit as st
import time


st.set_page_config(page_title="Input Coffee",page_icon="chart_with_upwards_trend",layout="wide")

col1,col2 = st.columns([1,1])
user = col1.text_input(label="", placeholder="Username")
user_pw = col1.text_input(label="", type="password", placeholder="Password")
login = col1.checkbox("Login", help="You are logged in while this checkbox is ticked")
