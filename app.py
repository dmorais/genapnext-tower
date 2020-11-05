import streamlit as st
import awesome_streamlit as ast
import streamlit.components.v1 as components
import os
import src.pages.home 
import src.pages.workflow_run
import src.pages.job_info
import src.pages.settings
from src.pages.sessionstate import *

from src.pages.util.web_helper import *

PAGES = {
    "Home": src.pages.home.main,
    "Settings": src.pages.settings.main,
    "Workflows": src.pages.workflow_run.main,
    "Jobs": src.pages.job_info.main,

}


def main():
    
     
    st.markdown(f'<h1 style="text-align:center;">GenAP Nextflow Tower</h1>', unsafe_allow_html=True)
    hide_none()

    state = get_state()

    if state.user != "user name" and state.user is not None:

         st.markdown(f'<p style="text-align:right;">Hi <b>{state.user}<b>!</p>', unsafe_allow_html=True)
     
    st.sidebar.title("Navigaton")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    st.write(PAGES[selection](state))
    
    state.sync()

if __name__ == "__main__":
    main()
