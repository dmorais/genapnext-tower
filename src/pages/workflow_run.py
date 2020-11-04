import os
import os.path

import streamlit as st
import awesome_streamlit as ast
import streamlit.components.v1 as components
from PIL import Image
import base64
import subprocess
import time
import namegenerator

from . import SessionState
from src.pages.util.web_helper import *
from src.pages.util.data_parsers import get_user_dict, add_new_user,create_app_dirs

import configparser

config = configparser.ConfigParser()
config.read('src/pages/configs/pipeline_config.ini')
BASE_DIR = config["pipeline"]["base_dir"]  # Local where all pipelines are installed


def prepare_job(pipeline_name, user_base_dir, random_name, config_name):

    
    st.header("Set Job Parameters")
    html = r"<small>If you don't know the requerements of your Workflow, leave the default value: <b>5GB of RAM, 24hrs and 6 CPUS</b></small>"
    st.markdown(html, unsafe_allow_html=True)
    
    mem = st.slider("Memory (GB)", 1, 128, 5, 1)
    time = st.slider("Time", 1, 120, 24, 1)
    cpu = st.slider("CPUs", 1, 24, 6, 1)
    
    st.write(random_name)
    
    
    if st.button("Create run file"):
        slurm_file =  open(os.path.join(user_base_dir, random_name + "_run_" + pipeline_name + ".sh" ), 'w')
      
        command = f"""#!/bin/bash
#SBATCH --time={time}
#SBATCH --mem={mem}G
#SBATCH --cpus-per-task={cpu} 

export RSNT_ARCH=avx2
source /cvmfs/soft.computecanada.ca/config/profile/bash.sh
module load nextflow

nextflow -C {config_name} -log out/nextflow_reports/{random_name}.log run vib-singlecell-nf/vsn-pipelines  -entry {pipeline_name} -name {random_name} -with-report out/nextflow_reports/{random_name}_execution_report.html \
-with-trace out/nextflow_reports/{random_name}_execution_trace.txt 
"""

        slurm_file.write(command)
        slurm_file.close()
   
        html2 = f"<small>Job script ({random_name}) was created</small>"
        st.markdown(html2, unsafe_allow_html=True)


def pipeline_svg(pipeline_name):
    """
        Load svg workflow of each pipeline (when available)
        :param pipeline_name: Pipeline name from the config file
        :return:
    """

    list_of_svg = config["pipeline"]["svg"].split("\n")
    
    if pipeline_name in list_of_svg:
        st.header("This is the " + pipeline_name + " Workflow")
        file = open(os.path.join(BASE_DIR, pipeline_name + ".svg"), 'r')
        svg = file.read()

        state = st.radio("Show/Hide Workflow", ["Hide", "Show"], 0)
        if state == "Show":
            _render_svg(svg)

    else:
        st.info("No Workflow svg image available for this Pipeline.")


def _render_svg(svg):
    """
        Render svg workflow of each pipeline (when available)
        :param svg: svg file object
        :return:
    """

    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img  width="1000" height="600" src="data:image/svg+xml;base64,%s"/>' % b64

    # st.markdown(html, unsafe_allow_html=True)
    components.html(html, 
                    scrolling=True, 
                    height=800, 
                    width=1000)


def config_panel(pipeline_name, config_name):
    """
        Load base config of the pipeline and save the modified version of it
        :param pipeline_name: Pipeline name from the config file
        :return:
    """
  
    st.header("Config of " + pipeline_name + " pipeline")
    file = open(os.path.join(BASE_DIR,"single_sample.config"), 'r')

    code = file.read()
    session = SessionState.get(code=code)

    user_config = open(config_name, 'w')
    state = st.radio("Edit or show", ['Edit', 'Show', "Hide"], 1)

    if state == 'Edit':
        session.code = st.text_area('Edit code', session.code)

        if st.button('Save changes'):        
            
            user_config.write(session.code)
            user_config.close()
            st.write('saved')

    elif state == "Hide":
        st.write("")

    else:
        st.code(session.code)
        user_config.write(session.code)
        user_config.close()
  

def user_section():
    
    # Get user dictonary
    user_dict = get_user_dict(config["setup"]["app_dir"], config["setup"]["app_user"])

    # SELECT BOX
    st.markdown("<h2>Select your User name</h2>", unsafe_allow_html=True)
    user = st.selectbox('', tuple(user_dict.keys()))

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

    return user,user_dict[user]


@st.cache
def random_namegenerator():
    return namegenerator.gen()
    

def write():  
   
    random_name = random_namegenerator()
        
    # Load st custom css   
    local_css()

    # Hide humburger menu
    hide_hambuger_menu()

    st.title("GenAP-Next-Tower Jobs")

    st.markdown("<h1>Workflows</h1>", unsafe_allow_html=True)

    # User section (load/add new user)
    option,unix_user = user_section()

    #Create user dir
    user_base_dir = os.path.join(config["setup"]["base_dir"], unix_user)
    create_app_dirs(user_base_dir)


    if option != "user name":
        
        # Let user set a random job name
        user_random = st.text_input("Job Random Name (optional). If you leave it blank we will assing a random name for you." )

        if user_random != "":
            user_random = "-".join(user_random.strip().split())
            random_name = user_random

        st.header("Choose your pipeline")
        pipeline_name = st.selectbox(
         "",
         config["pipeline"]["pipelines"].split("\n")
        )  
        
        if pipeline_name != "None": 

            # Config name
            config_name = os.path.join(user_base_dir, random_name + "_" + pipeline_name + ".config")
            
            config_panel(pipeline_name, config_name)
            pipeline_svg(pipeline_name)  

            prepare_job(pipeline_name, user_base_dir, random_name, config_name)

