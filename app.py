"""simscale outdoor comfort app."""


import streamlit as st
import extra_streamlit_components as stx
from helper import get_host, load_local_css
import input_model_options
import input_parameters
import submit_to_pollination


st.set_page_config(
    page_title='Pollination Parametric Studies',
    page_icon='https://app.pollination.cloud/favicon.ico',
    initial_sidebar_state='collapsed',
)


def main():

    load_local_css('assets/style.css')
    # find the host the app is being run inside
    # we use host to adopt the user interface accordingly
    host = get_host()

    # title
    st.title('Pollination Parametric Studies')

    # navbar
    step = stx.stepper_bar(
        steps=['Getting Started', 'Input Parameters', 'Submit', 'Results'],
        is_vertical=False
    )

    hb_model = None
    if step == 0:
        hb_model = input_model_options.render(
            host, hb_model=st.session_state.get('hb_model', None)
        )
        if hb_model:
            st.session_state['hb_model'] = hb_model
            st.write(
                'The model is loaded! You can now move to the next step to set the '
                'input parameters.'
            )
    elif step == 1: 
        if not 'hb_model' in st.session_state:
            st.error( 
                'You must load a valid model first. Go back to step 1 and load a model.'
            )
        else:
            params = input_parameters.render(params=st.session_state.get('params', {}))
            st.session_state['params'] = params
    elif step == 2:
        if not 'params' in st.session_state:
            st.error(
                'You must set the input parameters for the study before submitting it '
                'to Pollination. Go back to step 2 to set the parameters.'
            )
        job = submit_to_pollination.render(
            st.session_state['hb_model'],
            st.session_state['params']
        )
    # elif step == 3:
    #     config_path = 'data/config_utci.json'
    #     result_path = 'data/utci'
    #     print(analysis_period())
    #     utci(analysis_period(), hbjson_path, config_path, result_path, target_folder,
    #          host)

# import streamlit.report_thread as ReportThread
# from streamlit.server.server import Server
from streamlit.server.server import Server, SessionInfo

current_server = Server.get_current()
session_infos = Server.get_current()._session_info_by_id.values()

for v in session_infos:
    print(v.session._session_data)
    # print(v.session.session_state)
    # print(v.session._state)

if __name__ == '__main__':
    main()
