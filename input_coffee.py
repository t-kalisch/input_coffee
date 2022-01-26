import streamlit as st
import time

@st.cache(suppress_st_warning=True)  # 👈 Changed this
def expensive_computation(a, b):
    # 👇 Added this
    st.write("Cache miss: expensive_computation(", a, ",", b, ") ran")
    time.sleep(5)  # This makes the function take 2s to run
    return a * b

a = 2
b = 20
res = expensive_computation(a, b)

st.write("Result:", res)
