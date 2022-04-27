import os
import streamlit.components.v1 as components

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "discrete_slider",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("discrete_slider", path=build_dir)


def discrete_slider(options, key=None):
    option = _component_func(options=options, key=key, default=0)
    return option


if not _RELEASE:
    import streamlit as st

    cars = ["Porsche", "Mercedes", "BMV", "Audi", "VW"]
    st.subheader("Develop Mode")
    selected_idx = discrete_slider(cars)
    st.markdown(f"You've selected: {cars[selected_idx]}")
