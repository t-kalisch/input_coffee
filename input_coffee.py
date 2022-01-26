import streamlit as st
import time

@st.cache(suppress_st_warning=True)  # 👈 Changed this
def expensive_computation(a, b):
    # 👇 Added this
    st.write("Cache miss: expensive_computation(", a, ",", b, ") ran")
    time.sleep(2)  # This makes the function take 2s to run
    return a * b

a = st.text_input()
b = st.text_input()
res = st.button(label="Calculate", on_click=expensive_computation(a, b))

st.write("Result:", res)
