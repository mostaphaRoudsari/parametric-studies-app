"""A module to create a UI for generating a collection of analysis parameters."""

from typing import Dict
import streamlit as st


def render(params: Dict = None):
    params = params
    default = list(params.keys())
    values = st.multiselect(
        'Select several parameters for parametric studies.',
        options=[
            'Window to wall ratio', 'Shade depth', 'Shade count', 'Wall R value', 'Roof R value'
            ], default=default or ['Window to wall ratio']
    )
    if 'Window to wall ratio' in values:
        # create input UI for window to wall ratio
        with st.container():
            st.header('Window to wall ratio parmeters')
            mn, mx, stp = st.columns(3)

            min_wwr = mn.slider('Minimum WWR (%)', min_value=10, max_value=80, step=5, value=40)
            max_wwr = mx.slider('Maximum WWR (%)', min_value=20, max_value=90, step=5, value=80)
            wwr_step = stp.slider('Step', min_value=5, max_value=20, step=5, value=10)
            if max_wwr < min_wwr:
                st.error('Minimum WWR must be smaller than Maximum WWR.')
            wwr_options = list(range(min_wwr, max_wwr + wwr_step, wwr_step))
            st.write(f'WWR values: {wwr_options}')
            params['Window to wall ratio'] = wwr_options
    if 'Shade count' in values:
        # create input UI for window to wall ratio
        with st.container():
            st.header('Shade count parmeters')
            mns, mxs, stps = st.columns(3)
            min_sc = mns.selectbox('Minimum number', [0, 1, 2, 3, 4], index=0)
            max_sc = mxs.selectbox('Maximum number', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], index=0)
            sc_step = stps.selectbox('Step', [1, 2, 3], index=0)
            sc_options = list(range(min_sc, max_sc + sc_step, sc_step))
            st.write(f'Shade count values: {sc_options}')
            params['Shade count'] = sc_options
    if 'Shade depth' in values:
        with st.container():
            st.header('Shade depth parmeters')
            mnsd, mxsd, stpsd = st.columns(3)
            min_sd = mnsd.selectbox('Minimum depth', [0, 0.5, 1], index=0)
            max_sd = mxsd.selectbox('Maximum depth', [0, 0.5, 1, 1.5, 2, 2.5, 3], index=0)
            sd_step = stpsd.selectbox('Step', [0.1, 0.2, 0.5], index=0, key='shade_depth_step')
            sd_options = [
                x / 10 for x in
                range(int(min_sd * 10), int((max_sd + sd_step) * 10), int(sd_step * 10))
            ]
            st.write(f'Shade depth values: {sd_options}')
            params['Shade depth'] = sd_options

    if 'Wall R value' in values:
        st.error('Changing wall R value is not supported yet.')

    total_runs = 1
    for d in params.values():
        total_runs *= len(d)
    st.title(f'Total number of runs: {total_runs}')
    return params
