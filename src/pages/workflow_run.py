import os
import os.path

import streamlit as st
import awesome_streamlit as ast
import streamlit.components.v1 as components
from streamlit import caching
from PIL import Image
import base64
import subprocess
import time
import namegenerator

from src.pages.util.web_helper import *
from src.pages.util.data_parsers import get_user_dict, add_new_user,create_app_dirs

import configparser

config = configparser.ConfigParser()
config.read('src/pages/configs/pipeline_config.ini')
BASE_DIR = config["pipeline"]["base_dir"]  # Local where all pipelines are installed 


def submit_job(state,pipeline_name, random_name):

    run_file_name = random_name + "_run_" + pipeline_name + ".sh"

   

    if st.button("Submit Job"):
               
        cmd = ['/home/dmorais/anaconda3/envs/pyjob/bin/python', '/home/dmorais/projects/pyjobs/pysubmitjon.py',
             '--user', state.unix_user, '-d', state.user_base_dir, '--files', run_file_name, '-p', pipeline_name
              ]
        try:
            proc = subprocess.Popen(cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    )
            
            stdout_value, stderr_value = proc.communicate()
            print(stdout_value, stderr_value)
        
        except NameError as e:
            print(e)
       
        if "Waiting for job on sacct" in str(stdout_value):
            st.write(f'job {run_file_name} has been submitted')

        caching.clear_cache()


def prepare_job(state,pipeline_name, user_base_dir, random_name, config_name):

    
    st.header("Set Job Parameters")
    html = r"<small>If you don't know the requerements of your Workflow, leave the default value: <b>5GB of RAM, 24hrs and 6 CPUS</b></small>"
    st.markdown(html, unsafe_allow_html=True)
    
    mem = st.slider("Memory (GB)", 1, 128, 5, 1)
    time = st.slider("Time", 1, 120, 24, 1)
    cpu = st.slider("CPUs", 1, 24, 6, 1)
    
    run_file_name = random_name + "_run_" + pipeline_name + ".sh"
    # run_file_name = create_run_file_name(random_name,random_name) # It needs to be cached
    
    
    if st.button("Create run file"):
        slurm_file =  open(os.path.join(user_base_dir, run_file_name ), 'w')


        command = f"""#!/bin/bash
#SBATCH --time={time}
#SBATCH --mem={mem}G
#SBATCH --cpus-per-task={cpu}
#SBATCH --job-name={random_name}  

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


def config_panel(state, pipeline_name, config_name):
    """
        Load base config of the pipeline and save the modified version of it
        :param pipeline_name: Pipeline name from the config file
        :return:
    """
  
    
    st.header("Config of " + pipeline_name + " pipeline")
    file = open(os.path.join(BASE_DIR,"single_sample.config"), 'r')

    code = file.read()
    # state.code = code

    
    state_radio = st.radio("Edit or show", ['Edit', 'Show template', 'Show mine (only displayed after editing)', "Hide"], 1)

    if state_radio == 'Edit':
        state.code = st.text_area('Edit code', code)

        if st.button('Save changes'):        
            user_config = open(config_name, 'w')
            user_config.write(state.code)
            user_config.close()
            st.write('saved')

    elif state_radio == "Hide":
        st.write("")
    elif state_radio == "Show template":
        st.code(code)
    else:
        st.code(state.code)
 

@st.cache()
def random_namegenerator():
   
    return namegenerator.gen()
    

def main(state):  
   
    
    random_name = random_namegenerator()
        
    # Load st custom css   
    local_css()

    # Hide humburger menu
    hide_hambuger_menu()
    hide_none()
    
    st.markdown("<h1>Workflows</h1>", unsafe_allow_html=True)
    
    if state.user != "user name"  and state.user is not None:       
        # Let user set a random job name
        user_random = st.text_input("Job Random Name (optional). If you leave it blank we will assing a random name for you." )

        if user_random != "":
            user_random = "-".join(user_random.strip().split())
            random_name = user_random

        st.markdown("<h3>Choose your Pipeline</h3>", unsafe_allow_html=True)
        pipeline_name = st.selectbox(
         "",
         config["pipeline"]["pipelines"].split("\n")
        )  
        
        if pipeline_name != "None": 
            # Config name
            config_name = os.path.join(state.user_base_dir, random_name + "_" + pipeline_name + ".config")
            
            config_panel(state, pipeline_name, config_name)
            pipeline_svg(pipeline_name)  
            prepare_job(state, pipeline_name, state.user_base_dir, random_name, config_name)    
            
                  
            submit_job(state,pipeline_name, random_name)
    else:
        st.info("Go to the Settings Page and Set or Add new User")
