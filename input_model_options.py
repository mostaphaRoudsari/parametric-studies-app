"""A module to provide options for input model.

    To start it supports uploading an HBJSON file, start from a sample box or
    link to the model from inside Rhino.

"""

import pathlib
import json

import streamlit as st
from pollination_streamlit_io import button, special
from honeybee.model import Model as HBModel

import viewer

def render(host: str = 'Web', temp_folder: str = 'data', hb_model: HBModel = None) -> HBModel:
    """Render the UI for uploading an input HBJSON model."""
    hb_model = hb_model
    source = st.session_state.get('hb_model_source', None)
    woking_dir = pathlib.Path(temp_folder)
    woking_dir.mkdir(parents=True, exist_ok=True)
    default_index = 0
    options = ['Upload a File', 'Use Geometry Wizard']
    if host.lower() == 'rhino':
        options.append('Link to Model in Rhino')
        default_index = len(options) - 1
    option = st.selectbox(
        'Select a method to input the analytic model', options=options,
        index=default_index
    )
    if option == 'Upload a File':
        uploaded_file = st.file_uploader(
            'Upload an HBJSON file.', type=['hbjson', 'json'],
            accept_multiple_files=False, key='app_input_model_file_uploader'
        )
        if uploaded_file:
            source = woking_dir.joinpath(uploaded_file.name)
            source.write_bytes(uploaded_file.read())
            hb_model = HBModel.from_dict(json.loads(source.read_text()))
            st.session_state['hb_model_source'] = source
    elif option == 'Link to Model in Rhino':
        # load the model from Rhino
        # token = special.sync(key='pollination-sync', delay=50)
        data = button.get(isPollinationModel=True, key='pollination-model')

        if data:
            model_data = json.loads(data)
            hb_model = HBModel.from_dict(model_data)
            source = woking_dir.joinpath(f'{hb_model.identifier}.hbjson')
            source.write_text(json.dumps(model_data))
            st.session_state['hb_model_source'] = source
    elif option == 'Use Geometry Wizard':
        st.session_state['hb_model_source'] = None
        st.warning('The geometry wizard is not supported yet. :(')

    if st.session_state.get('hb_model_source'):
        viewer.render(st.session_state['hb_model_source'].as_posix())

    return hb_model
