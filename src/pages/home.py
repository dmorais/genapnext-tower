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
# BASE_DIR = config["pipeline"]["base_dir"]  # Local where all pipelines are installed

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


