import os

import streamlit as st
import awesome_streamlit as ast
import streamlit.components.v1 as components
from PIL import Image
import base64
import subprocess
import time
import namegenerator

from src.pages.util.web_helper import *
from src.pages.util.data_parsers import get_user_dict, add_new_user,create_app_dirs, create_user_dict

import configparser

config = configparser.ConfigParser()
config.read('src/pages/configs/pipeline_config.ini')
BASE_DIR = config["pipeline"]["base_dir"]  # Local where all pipelines are installed


# def user_section(state):
    
#     # Get user dictonary
#     user_dict = get_user_dict(config["setup"]["app_dir"], config["setup"]["app_user"])

#     # SELECT BOX
#     st.markdown("<h2>Select your User name</h2>", unsafe_allow_html=True)
#     state.user = st.selectbox('', tuple(user_dict.keys()))

#     user_section = st.radio("Hide/show add new user", ['Show', "Hide"], 0)

#     if user_section == "Show":
#         unregistred_user = st.text_input("Add your user name: first_name last_name" ) 
    
#         if st.button("Add new user"):
#             if len(unregistred_user.split()) != 2:
#                 st.error("Must be in the first_name last_name format")
            
#             else:
#                 add_new_user(config["setup"]["app_dir"], config["setup"]["app_user"], unregistred_user)  
#                 st.button("Reload User List")
#     else:
#         st.write("")

#     state.unix_user = user_dict[state.user]

#     return 0



def main(state):
    
    # Set Up dirs and user list
    create_app_dirs(config["setup"]["app_dir"])
    create_user_dict(config["setup"]["app_dir"], config["setup"]["app_user"])
   
    # Load st custom css   
    local_css()

    # Hide humburger menu
    hide_hambuger_menu()

    hide_none()
    

    st.markdown("<h1>Home</h1>", unsafe_allow_html=True)


    # user_section(state)