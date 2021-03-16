# Mateusz Leputa March 2021
# Streamlit Space Program

import time

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from sim import World, Vehicle


earth = World()

rocket = Vehicle()
print(type(rocket))

rocket.place_on_surface(earth)


def main():

    i = 0
    dt = 0.05

    x = []
    y = []
    dy =[]
    dx = []
    t_arr= []
    t = 0
    alt = []
    range = []
    ang = []
    heading = []
    rocket.theta = 0

    thrust = 1

    st.set_page_config(page_title='SoundOff',
                       initial_sidebar_state="collapsed",
                       layout="wide"
                       )
    page = st.sidebar.title("Settings")
    while(i<2*160000):
        rocket.step(thrust,earth,dt)
        t_arr.append(t)
        heading.append(rocket.heading)
        x.append(rocket.x)
        y.append(rocket.y-earth.radius)

        dy.append(rocket.dy)
        dx.append(rocket.dx)
        ang.append(rocket.theta)

        wx,wy = earth.get_location()
        rx,ry = rocket.get_location()

        distance = np.sqrt((wx-rx)**2+(wy-ry)**2)
        alt.append(distance - earth.radius)
        range.append(np.arctan2((rx),(ry))*earth.radius)

        angle = (1-np.exp(-t/160))*120
        thrust = {"theta":angle}

        if t > 140:
            thrust = {"thrust":0}
            rocket.drag_coeff = 0.8
        if t > 161 and t < 163:
            angle = np.degrees(rocket.heading - np.pi)
            thrust = {"thrust":1,"theta":angle}
        if distance-earth.radius < 2200 and t > 100: #1750
            angle = np.degrees(rocket.heading - np.pi)
            thrust = {"thrust":1,"theta":angle}
        if distance < earth.radius and t > 10:
            print("crash!")
            break

        t+=dt
        i+=1
    df = pd.DataFrame()
    df["t"] = t_arr
    df["x"] = x
    df["y"] = y
    df["dx"] = dx
    df["dy"] = dy
    df["dxy"] = np.sqrt(np.power(dy,2)+np.power(dx,2))
    df["alt"] = alt
    df["range"] = range
    df["heading"] = heading

    template = "plotly_white"

    fig0 = px.line(df, x="t", y=["x","y"],template=template)
    st.plotly_chart(fig0)
    fig1 = px.line(df, x="x", y="y",template=template)
    st.plotly_chart(fig1)
    fig2 = px.line(df, x="range", y="alt",template=template)
    st.plotly_chart(fig2)
    fig3 = px.line(df, x="t", y="heading",template=template)
    st.plotly_chart(fig3)
    fig4 = px.line(df, x="t", y=["dx","dy","dxy"],template=template)
    st.plotly_chart(fig4)

    st.button("Re-run")
    # draw_circle = plt.Circle((0.0, 0.0-earth.radius), earth.radius,fill=False)

if __name__ == '__main__':
    main()
