import streamlit as st


def load_local_css(file_name):
    """Load a local css file."""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def get_host() -> str:
    """Find the host the app is running on.
    
    It can be Rhino, Revit or Web.
    """
    st_query = st.experimental_get_query_params()
    return st_query['__platform__'][0] if '__platform__' in st_query else 'web'
