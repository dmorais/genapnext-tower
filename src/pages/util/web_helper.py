import streamlit as st
from jinja2 import Environment, FileSystemLoader
import awesome_streamlit as ast
import streamlit.components.v1 as components
import os

def local_css():
    file_name = "src/pages/jinja-templates/css/st_style.css"
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True) 


def load_jinja(jinja_template):
    """
        Prepare a jinja template to be rendered
        :param jinja_template: html file with jinja code on it
        :return template: a loaded jinja object
    """
    env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(jinja_template)

    return template


def hide_hambuger_menu():
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>

    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 