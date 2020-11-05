import os

import streamlit as st
import awesome_streamlit as ast
import streamlit.components.v1 as components

from src.pages.util.data_parsers import get_db_stats
from src.pages.util.web_helper import *


@st.cache
def get_trace(file_path, run_name):
    """
    Get and parse trace file
    :param file_path: Full path to submit dir
    :param run_name: random run name created at submission time (trace file depends on this name) 
    :return parsed_file: 
    """
    
    parsed_file = []
    fh = open(os.path.join(file_path, run_name + "_execution_trace.txt"))

    for line in fh:
        record = line.strip().split("\t")

        if record[0] == "task_id":
            parsed_file.append(record)
            continue

        record[1] = record[1].split(":")[-1].replace("__","-")
        record[3] = record[3][0]   

        parsed_file.append(record) 

    return parsed_file

@st.cache
def get_report(file_path, run_name):
    """
    Get and parse trace file
    :param file_path: Full path to submit dir
    :param run_name: random run name created at submission time (trace file depends on this name) 
    :return report: html page with the full report 
    """
    fh = open(os.path.join(file_path, run_name + "_execution_report.html"))
    report = fh.read()

    return report


def main(state):

    # Load st custom css   
    local_css()

    # Hide humburger menu
    hide_hambuger_menu()
    hide_none()

    if state.user != "user name" and state.user is not None:
        trace = 'No trace yet'
        jobs = get_db_stats()
        
        html_template = ''

        st.title("Job Reports")
        
        # SELECT BOX
        st.markdown("<h3>Select Job to display</h3>", unsafe_allow_html=True)
        option = st.selectbox('', tuple(jobs.keys()))

        page_report = st.radio("Select", ['Trace per Job', 'Full Report'])

        if page_report == "Trace per Job":
            # Update page 
            update = st.button("Update Status")
            
            # Get trace file
            if jobs[option]["state"] == "Complete" or jobs[option]["state"] == "Failed":
                trace = get_trace(jobs[option]["submission_dir"], jobs[option]["run_name"])
            
            # load jinja
            template = load_jinja('src/pages/jinja-templates/job_info.html')

            # render template
            html_template = template.render(jobs=jobs,  trace=trace, option=option)

        else:
            if jobs[option]["state"] == "Complete" or jobs[option]["state"] == "Failed":
                html_template = get_report(jobs[option]["submission_dir"], jobs[option]["run_name"])

            else:
                html_template = f'<h2>Job State is {jobs[option]["state"]}.</h2><h2>No report just yet</h2>'


        components.html(html_template, 
                            scrolling=True, 
                            height=1000, 
                            width=1200)
            
        
        st.markdown(f'<div class="footer p-3">All rights reveserved to ©GenAP</div>', unsafe_allow_html=True)

    else:
        st.info("Go to the Settings Page and Set or Add new User")


if __name__ == "__main__":
    write()