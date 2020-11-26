import os

import streamlit as st
import awesome_streamlit as ast
import streamlit.components.v1 as components

from src.pages.util.web_helper import *
from src.pages.util.data_parsers import get_user_dict, add_new_user,create_app_dirs, create_user_dict

import configparser

config = configparser.ConfigParser()
config.read('src/pages/configs/pipeline_config.ini')




def user_section(state):
    
    # Get user dictonary
    user_dict = get_user_dict(config["setup"]["app_dir"], config["setup"]["app_user"])

    # SELECT BOX
    st.markdown("<h3>Select your User name</h3>", unsafe_allow_html=True)
    state.user = st.selectbox('', tuple(user_dict.keys()))

    user_section = st.radio("Hide/show add new user", ['Show', "Hide"], 0)

    if user_section == "Show":
        unregistred_user = st.text_input("Add your user name: first_name last_name" ) 
    
        if st.button("Add new user"):
            if len(unregistred_user.split()) != 2:
                st.error("Must be in the first_name last_name format")
            
            else:
                add_new_user(config["setup"]["app_dir"], config["setup"]["app_user"], unregistred_user)  
                st.button("Reload User List")
    else:
        st.write("")

    state.unix_user = user_dict[state.user]

    


def main(state):

    # Style  
    local_css()  
    hide_hambuger_menu()
    hide_none()

    st.markdown("<h1>Settings</h1>", unsafe_allow_html=True)
    
    # Set Up dirs and user list
    create_app_dirs(config["setup"]["app_dir"])
    create_user_dict(config["setup"]["app_dir"], config["setup"]["app_user"])    

    user_section(state)

    #Create user dir
    state.user_base_dir = os.path.join(config["setup"]["base_dir"], state.unix_user)
    create_app_dirs(state.user_base_dir)




if __name__ == "__main__":
    main()