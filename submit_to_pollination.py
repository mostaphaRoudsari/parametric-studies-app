"""A module to create the runs and submit the job to Pollination.

This module needs to be improved in the future. We should provide a better wrapper
for submitting jobs from pollination_streamlit

"""
from typing import Any, Dict
import streamlit as st
import pathlib
import time

from queenbee.job.job import JobStatusEnum
from pollination_streamlit.api.client import ApiClient
from pollination_streamlit.interactors import Job, NewJob, Recipe

from honeybee.model import Model as HBModel

def render(base_model: HBModel, params: Dict = None):
    run_params = generate_design_options(base_model, params)
    new_job = create_job(run_params)
    if new_job:
        submit = st.checkbox('Submit to Pollination')
        if submit:
            running_job = submit_job(new_job)
            time.sleep(2)
            st.markdown(
                f'Check out the simulations here [here](https://app.pollination.cloud/projects/{running_job.owner}/{running_job.project}/jobs/{running_job.id})'
            )
    return


def generate_design_options(base_model: HBModel, params: Dict = None) -> Dict:
    """Generate design options based on the initial model and the input parameters."""
    wwrs = params['Window to wall ratio']
    # shd_depths = params['Shade depth']
    # shd_counts = params['Shade count']
    faces_with_aperture = [face for face in base_model.faces if face.apertures]
    for face in faces_with_aperture:
        for wwr in wwrs:
            pass
    return [{'model': str(st.session_state['hb_model_source'].resolve())}]


def _get_annual_energy_recipe(api_client):
    return Recipe('ladybug-tools', 'annual-energy-use', 'latest', api_client)


def create_job(run_params: Dict[str, Any]) -> NewJob:
    api_key = st.text_input('Enter your Pollination API key', type='password')
    api_client = ApiClient(api_token=api_key)
    if not (api_key and api_client):
        return
    recipe = _get_annual_energy_recipe(api_client)
    st.header('Submission information')
    owner = st.text_input('Account name')
    project = st.text_input('Project name', value='demo')
    st.header('Location information')
    epw = st.file_uploader('Upload EPW file', type=['epw'])
    if epw:
        epw_file = pathlib.Path(f'{epw.name}')
        epw_file.write_bytes(epw.read())
    ddy = st.file_uploader('Upload DDY file', type=['ddy'])
    if ddy:
        ddy_file = pathlib.Path(f'{ddy.name}')
        ddy_file.write_bytes(ddy.read())
    if not (owner and epw and ddy):
        return

    new_job = NewJob(owner, project, recipe, client=api_client)

    for param in run_params:
        param['epw'] = str(epw_file.resolve())
        param['ddy'] = str(ddy_file.resolve())

    # TODO: upload the artifacts

    # create all the run options
    new_job.arguments = run_params

    return new_job


def submit_job(job: NewJob) -> Job:
    raise ValueError('Submit job has not been implemented.')
    running_job = job.create()
    return running_job
