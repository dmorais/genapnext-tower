import streamlit as st
from jinja2 import Environment, FileSystemLoader
import awesome_streamlit as ast
import streamlit.components.v1 as components
import os

def load_jinja(jinja_template):
    """
        Prepare a jinja template to be rendered
        :param jinja_template: html file with jinja code on it
        :return template: a loaded jinja object
    """
    env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(jinja_template)

    return template


def write():
    
    users = ["David", "Gabi", "Emma"]

    # load jinja
    template = load_jinja('src/pages/jinja-templates/workflow_run.html')

    # render template
    html_template = template.render(users=users)

    components.html(html_template, 
                    scrolling=True, 
                    height=10000, 
                    width=1000)