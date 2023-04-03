import streamlit as st
from random import random


if 'all_messages' not in st.session_state:
    st.session_state.all_messages = []

st.write("All messages:")
for message in st.session_state.all_messages:
    st.write(message)



 
txt = st.text_area('Text to analyze', '''
    It was the best of times, it was the worst of times, it was
    the age of wisdom, it was the age of foolishness, it was
    the epoch of belief, it was the epoch of incredulity, it
    was the season of Light, it was the season of Darkness, it
    was the spring of hope, it was the winter of despair, (...)
    ''',
    )
    )




# Runs once during app start
if "variables_setup" not in st.session_state:
    st.session_state["variables_setup"] = True
    st.session_state.input_message_key = str(random())

# message input
input_message = st.text_input(
    label = "-",
    label_visibility = "collapsed",
    key=st.session_state.input_message_key,
)

if input_message:
    st.session_state.input_message_key = str(random())
    # -- PROCESS YOUR TEXT HERE -- 
    st.session_state.all_messages.append(input_message)
    st.experimental_rerun()




