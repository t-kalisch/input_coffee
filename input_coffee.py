from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

import datetime
from datetime import date
#from data_collection import *
#import matplotlib.pyplot as plt

"""
# Please input a coffee break.
etstsertestsetrestststdsfasdfds
"""

def start_break():
    return
    
drinker=st.text_input(label="", type="default", placeholder="Name")
start = st.button("Start break", help="Start a coffee break for yourself", on_click=start_break())
    
