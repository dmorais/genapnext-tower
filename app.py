import streamlit as st
import awesome_streamlit as ast
import streamlit.components.v1 as components
import os
import src.pages.home 
import src.pages.workflow_run
import src.pages.job_info
import src.pages.settings
from src.pages.sessionstate import *

# from streamlit.hashing import _CodeHasher
# from streamlit.report_thread import get_report_ctx
# from streamlit.server.server import Server
# import streamlit as st
from src.pages.util.web_helper import *

PAGES = {
    "Home": src.pages.home.main,
    "Settings": src.pages.settings.main,
    "Workflows": src.pages.workflow_run.main,
    "Jobs": src.pages.job_info.main,

}


def main():
    
    st.title("GenAP-Next-Tower")
    hide_none()

    state = get_state()
    st.write("** Current user:**", state.unix_user)
     
    st.sidebar.title("Navigaton")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    st.write(PAGES[selection](state))
    
    state.sync()


# class _SessionState:

#     def __init__(self, session, hash_funcs):
#         """Initialize SessionState instance."""
#         self.__dict__["_state"] = {
#             "data": {},
#             "hash": None,
#             "hasher": _CodeHasher(hash_funcs),
#             "is_rerun": False,
#             "session": session,
#         }

#     def __call__(self, **kwargs):
#         """Initialize state data once."""
#         for item, value in kwargs.items():
#             if item not in self._state["data"]:
#                 self._state["data"][item] = value

#     def __getitem__(self, item):
#         """Return a saved state value, None if item is undefined."""
#         return self._state["data"].get(item, None)
        
#     def __getattr__(self, item):
#         """Return a saved state value, None if item is undefined."""
#         return self._state["data"].get(item, None)

#     def __setitem__(self, item, value):
#         """Set state value."""
#         self._state["data"][item] = value

#     def __setattr__(self, item, value):
#         """Set state value."""
#         self._state["data"][item] = value
    
#     def clear(self):
#         """Clear session state and request a rerun."""
#         self._state["data"].clear()
#         self._state["session"].request_rerun()
    
#     def sync(self):
#         """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

#         # Ensure to rerun only once to avoid infinite loops
#         # caused by a constantly changing state value at each run.
#         #
#         # Example: state.value += 1
#         if self._state["is_rerun"]:
#             self._state["is_rerun"] = False
        
#         elif self._state["hash"] is not None:
#             if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
#                 self._state["is_rerun"] = True
#                 self._state["session"].request_rerun()

#         self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


# def _get_session():
#     session_id = get_report_ctx().session_id
#     session_info = Server.get_current()._get_session_info(session_id)

#     if session_info is None:
#         raise RuntimeError("Couldn't get your Streamlit Session object.")
    
#     return session_info.session


# def _get_state(hash_funcs=None):
#     session = _get_session()

#     if not hasattr(session, "_custom_session_state"):
#         session._custom_session_state = _SessionState(session, hash_funcs)

#     return session._custom_session_state


if __name__ == "__main__":
    main()
