"""A module to add a Pollination 3D viewer to the app."""

import streamlit as st
from pathlib import Path
from honeybee_vtk.model import Model as VTKModel
from streamlit_vtkjs import st_vtkjs


# TODO: add caching here to render the model only once
st.cache()
def render(file_path: str, key='3d_viewer', subscribe=False):
    """Render the 3D viewer."""
    if not file_path:
        return

    vtkjs_folder = Path('data')
    vtkjs_folder.mkdir(parents=True, exist_ok=True)
    hb_file = Path(file_path)
    model = VTKModel.from_hbjson(hb_file.as_posix())
    vtkjs_file = vtkjs_folder.joinpath(f'{hb_file.stem}.vtkjs')
    if not vtkjs_file.is_file():
        model.to_vtkjs(
            folder=vtkjs_folder.as_posix(),
            name=hb_file.stem
        )
    print(f'Updating 3D viewer: {key}')
    st_vtkjs(
        content=vtkjs_file.read_bytes(),
        key=key, subscribe=subscribe
    )
