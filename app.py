# Mateusz Leputa March 2021
# Streamlit Space Program

import time

import streamlit as st
import numpy as np

from sim import World, Vehicle


earth = World()

rocket = Vehicle()

rocket.place_on_surface(earth)

def main():
    st.set_page_config(page_title='SoundOff',
                       initial_sidebar_state="collapsed",
                       layout="wide"
                       )
    page = st.sidebar.title("Settings")

    progress_bar = st.sidebar.progress(0)

    status_text = st.sidebar.empty()
    last_rows = np.array([rocket.y-earth.radius])
    chart = st.line_chart(last_rows)
    chart2 = st.line_chart(np.array([rocket.dy]).astype("float16"))
    time_stamp = 0
    sim_time = 50
    dt = 0.1

    for i in range(1, int(sim_time/dt)):
        thrust = 1.0
        if i > 60:
            thrust = 0.0
        rocket.step(thrust,earth,dt)
        time_stamp+=dt

        new_rows = np.array([rocket.y-earth.radius])
        new_rows2 = np.array([rocket.dy]).astype("float16")
        status_text.text("%i%% Complete" % i)

        chart.add_rows(new_rows)
        chart2.add_rows(new_rows2)

        progress_bar.progress(i/(sim_time/dt))
        last_rows = new_rows

        # print(last_rows)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


if __name__ == '__main__':
    main()
