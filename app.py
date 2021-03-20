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
    dt = 0.1

    x = []
    y = []
    dy = []
    dx = []
    t_arr = []
    t = 0
    alt = []
    range = []
    ang = []
    heading = []
    rocket.theta = 1

    thrust = 1



    st.set_page_config(page_title='Streamlit Space Program',
                       initial_sidebar_state="collapsed",
                       layout="wide",
                       page_icon=":rocket:"
                       )
    col1, colc, col2 = st.beta_columns((1, 5, 1))


    colc.markdown('<h1 style="text-align: center;">Stramlit Space Porgram V 0.1</h1>',
                  unsafe_allow_html=True)
    colc.markdown("""*Stramlit Space Program* was inspired by observing SpaceX launches. \
                    I wanted to see how difficult it would be to simulate and control a simplified model of a rocket with parameters akin to the Falcon-9. \
                    I think it has resulted in a fun tool to play around with.""", unsafe_allow_html=False)
    colc.markdown(""" ## The Simulation""", unsafe_allow_html=False)
    colc.markdown("""The environment for the simulation is a simplified model of earth with a basic atmosphere model (pressure only) based on the equations from [here](https://www.grc.nasa.gov/www/k-12/rocket/atmosmet.html). \
                    This lets the rocket experience different drag at different altitudes. The atmosphere is simulated up to an altitude of around 120 km where it is nearly negligible.
                    """, unsafe_allow_html=False)
    colc.markdown("""The gravity changes with altitude according to the [Newtonian universal law of gravitation](https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation).
                     """, unsafe_allow_html=False)
    colc.markdown("""The two forces are applied radially from the surface of the earth, centred around the origin.""", unsafe_allow_html=False)

    # colc.latex(r'''F=G\frac{{m_1}{m_2}}{{r^2}}''') # too much tbh its in the link

    colc.markdown(""" ## The Rocket""", unsafe_allow_html=False)
    colc.markdown("""The rocket (for now at least) has 2 continuous control variables: angle and thrust. The angle determines the direction the thrust is applied,
                    the angle is the direction in the absolute cartesian grid of the environment (i.e not with respect to the tangent of the earth).
                    Thrust has a value between 0.0 and 1.0, where one corresponds to the max thrust of the vehicle specification. The rocket also has a grid fin deployment control variable which changes the coefficient of drag from 0.3 to 0.8 (guesstimated values :shrug:).
                    """, unsafe_allow_html=False)

    colc.markdown("""Other parameters include:\n* Wet Mass -- 549,000 kg\n* Dry Mass -- 109,000 kg\n* Fuel Mass -- 440,000 kg\n* Thrust -- 8027 kN\n* Burn Time at full thrust -- 162 seconds""", unsafe_allow_html=True)
    colc.markdown(""" ## Roadmap""", unsafe_allow_html=False)
    colc.markdown("""""", unsafe_allow_html=False)

    colc.markdown('<h1 style="text-align: center;">Vehicle Program</h1>',
                  unsafe_allow_html=True)
    col1, colc0,colc1, col2 = st.beta_columns((1,2,3, 1))

    default_command ="""{
    '0': {'condition': {'t': {'>': 0, '<=': 10}}, 'action': {'thrust': 1}},
    '1': {'condition': {'t': {'>': 10, '<=': 20}}, 'action': {'thrust': 0}}
     }"""
    commands = colc1.text_area("Program Input",default_command , height = 300)

    if colc1.button("Run"):


        while(i < 2*1600000):
            rocket.step(commands, earth, dt)
            t_arr.append(t)
            heading.append(rocket.heading)
            x.append(rocket.x)
            y.append(rocket.y-earth.radius)

            dy.append(rocket.dy)
            dx.append(rocket.dx)
            ang.append(rocket.theta)

            wx, wy = earth.get_location()
            rx, ry = rocket.get_location()

            distance = np.sqrt((wx-rx)**2+(wy-ry)**2)

            alt.append(distance - earth.radius)
            range.append(np.arctan2((rx), (ry))*earth.radius)

            # angle = (1-np.exp(-t/160))*120
            # thrust = {"theta": angle}

            # if t > 140:
            #     thrust = {"thrust": 0}
            #     rocket.drag_coeff = 0.8
            # if t > 161 and t < 163:
            #     angle = np.degrees(rocket.heading - np.pi)
            #     thrust = {"thrust": 1, "theta": angle}
            # if distance-earth.radius < 2200 and t > 100:  # 1750
            #     angle = np.degrees(rocket.heading - np.pi)
            #     thrust = {"thrust": 1, "theta": angle}
            if distance < earth.radius and t > 10:
                print("crash!")
                break

            t += dt
            i += 1
        df = pd.DataFrame()
        df["t"] = t_arr
        df["x"] = x
        df["y"] = y
        df["dx"] = dx
        df["dy"] = dy
        df["dxy"] = np.sqrt(np.power(dy, 2)+np.power(dx, 2))
        df["alt"] = alt
        df["range"] = range
        # np.degrees(np.arctan2((alt+(earth.radius*np.ones(len(alt),))),range)- heading)
        df["heading"] = np.degrees(heading)
        df["ang"] = ang



        template = "plotly_dark"

        # columns for better alignment





        _,col1, col2,_ = st.beta_columns((1,2.5,2.5,1))




        fig2 = px.line(df, x="range", y="alt", template=template, title="Range and Altitude",
                       labels={
                           "range": "Range (m)",
                           "alt": "Altitude (m)"}
                       )
        fig2.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            })
        col1.plotly_chart(fig2, use_container_width=True)
        col1.markdown('Range is the displacement following the surface of the earth, altitude is the distance above the surface of the earth.', unsafe_allow_html=False)

        fig1 = px.line(df, x="x", y="y", template=template, title="X and y displacements in the cartesian grid",
                       labels={
                           "x": "X-displacement (m)",
                           "y": "Y-displacement (m)"})
        fig1.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            })
        col1.plotly_chart(fig1, use_container_width=True)

        col1.markdown(
            'This graph shows the same information but in an absolute cartesian form. Useful for seeing how the rocket flies around the curvuture of the earth.', unsafe_allow_html=False)

        fig0 = px.line(df, x="t", y=["alt", "range"], template=template, title="Altitude and range displacements.",
                       labels={
            "Species": "components",
            "alt": "altitude - displacement (m)",
            "range": "range - displacement (m)",
            "t": "Mission time (s)"
        })
        fig0.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            })

        col1.plotly_chart(fig0, use_container_width=True)
        col1.markdown(
            'Same information as above but split into x and y co-ordinates; plotted against mission time.', unsafe_allow_html=False)

        fig4 = px.line(df, x="t", y=["dx", "dy", "dxy"], template=template, title="X and y displacements against time in the cartesian grid",
                       labels={
            "dx": "x - velocity (m/s)",
            "dy": "y - velocity (m/s)",
            "dxy": "magnitude velocity (m/s)",
            "t": "Mission time (s)"
        })
        fig4.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            })

        col2.plotly_chart(fig4, use_container_width=True)
        col2.markdown('x,y and magnitude velocity against mission time.', unsafe_allow_html=False)

        fig3 = px.line(df, x="t", y=["heading","ang"], template=template, title="Heading (in the absolute cartesian grid)",
                       labels={
                           "heading": "Heading (deg)",
                           "ang": "Vehicle direction (deg)",
                           "t": "Mission time (s)"
                       })
        fig3.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            })
        col2.plotly_chart(fig3, use_container_width=True)
        col2.markdown('Heading (in the absolute cartesian grid).', unsafe_allow_html=False)




if __name__ == '__main__':
    main()
