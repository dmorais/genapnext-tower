import streamlit as st
import awesome_streamlit as ast
import streamlit.components.v1 as components
import os
import src.pages.home
import src.pages.workflow_run
import src.pages.job_info



PAGES = {
    "Home": src.pages.home,
    "Workflows": src.pages.workflow_run,
    "Job Info": src.pages.job_info,
}



def main():
    
    st.sidebar.title("Navigaton")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)

    


if __name__ == "__main__":
    main()