# Mateusz Leputa March 2021
# Streamlit Space Program

import time

import streamlit as st
import numpy as np
import pandas as pd

from sim import World, Vehicle


earth = World()

rocket = Vehicle()
print(type(rocket))

rocket.place_on_surface(earth)

def main():
    st.set_page_config(page_title='SoundOff',
                       initial_sidebar_state="collapsed",
                       layout="wide"
                       )
    page = st.sidebar.title("Settings")

    progress_bar = st.sidebar.progress(0)

    last_rows = np.array([rocket.y-earth.radius])

    time_stamp = 0
    sim_time = 50
    dt = 0.1
    i = 0

    # while(True):

    st.button("Re-run")


if __name__ == '__main__':
    main()
