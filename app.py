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

    thrust = 0



    st.set_page_config(page_title='Streamlit Space Program',
                       initial_sidebar_state="collapsed",
                       layout="wide",
                       page_icon=":rocket:"
                       )
    col1, colc, col2 = st.beta_columns((1, 5, 1))


    colc.markdown('<h1 style="text-align: center;">Stramlit Space Program V 0.1</h1>',
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

    colc.markdown("""Other parameters include:\n* Wet Mass -- 549,000 kg\n* Dry Mass (inc. second stage) -- 109,000 kg\n* Fuel Mass -- 440,000 kg\n* Thrust -- 8027 kN\n* Burn Time at full thrust -- 162 seconds""", unsafe_allow_html=True)
    colc.markdown(""" ## Roadmap for the app""", unsafe_allow_html=False)
    colc.markdown("""Features I will be adding soon include:\n- Multi stage vehicles\n- More vehicle presets - coming soon!\n- Environment to use with the AI gym, so that you can train and upload your tensorflow model.\n- Rule configurator""")
    colc.markdown("""If you like my work and want to keep up to date, have ideas for features or want to see the code consider starring my [repo](https://github.com/MatInGit/StreamlitSpaceProgram) and if you really like my work you can [buy me a coffee](https://www.buymeacoffee.com/MatInSpace)""", unsafe_allow_html=False)

    colc.markdown('<h1 style="text-align: center;">Vehicle Control</h1>',
                  unsafe_allow_html=True)
    col1, colc1, col2 = st.beta_columns((1,6,1))

    colc1.markdown("""You can program the rocket behaviour in the window below.
    The rocket program is dictionary of dictionaries, at the highest level the dictionary contains unique `rules`. Each `rule` in the dictionary has the following structure:
    """)

    code = """
    ‘UID0’:{‘condition’: {‘var’:{‘>’:0,’<=’:10}},’action’:{‘var_to_set’:1.0}}
    """


    colc1.code(code,language = 'python')

    colc1.markdown("""`UID0` can be any *uniqe* string, it must be uniqe otherise the parser might overwrite the rules.
    \n`var` is the variable that is being evaluated for the rule to activate, this can be anything from the follwoing list:\n- `t` -- Mission time\n- `alt` -- Altitude\n- `range`-- Downrange distance\n- `heading`-- Heading\n- `dalt`-- Rate of change of altitude\n- `drange`-- Rate of change of downrange distance\n""")
    colc1.markdown("""`val_to_set` stands for any of the variables that you can control, you can have multiple values in one rule:\n- `thrust`-- value between 0.0 and 1.0 (zero to max thrust respectively)\n- `angle` -- the direction the thrust is applied, can be an absolute angle between -180 and 180, `prograde` or `retrograde`\n- `gridfins` -- increase coefficent of drag when deployed, the options are `deploy` or `fold`\n- `separation` -- When this keyword is used the mass eqivalent of a Falcon-9 second stage is subrtacted from the vehicle mass. The accimplanying dictionary has to be empty `'separation:{}'`. In the future this will deploy a second vehicle to control.
    """)


    default_command ="""{
    '0': {'condition': {'t': {'>': 0, '<=': 150}}, 'action': {'thrust': 1,'angle':10}},
    '1': {'condition': {'t': {'>': 151, '<=': 200}}, 'action': {'thrust': 0,'angle':'retrograde','separation':{}}},
    '2': {'condition': {'alt': {'>': 0, '<=': 3000},'t':{'>':100},'drange':{'>':10}}, 'action': {'thrust': 1,'angle':'retrograde'}}
     }"""
    commands = colc1.text_area("Program Input",default_command , height = 300)

    ry = colc1.slider("Initial altitude (km)",0,500,0)
    rdy = colc1.slider("Initial vertical velocity (m/s)",-10000,10000,0)
    rdx = colc1.slider("Initial horizontal velocity (m/s)",-10000,10000,0)

    rocket.y = earth.radius + ry*1000
    rocket.dx = rdx
    rocket.dy = rdy

    if colc1.button("Run"):


        while(i < 4*16000):

            rocket.step(commands,earth,dt)

            wx, wy = earth.get_location()
            diffx = -wx + rocket.x
            diffy = -wy + rocket.y
            distance = np.sqrt(np.power(diffx,2)+np.power(diffy,2))

            if distance < earth.radius and t > 10:
                print("crash!")
                break

            t += dt
            i += 1


        template = "plotly_dark"


        # columns for better alignment
        _,col1, col2,_ = st.beta_columns((1,3,3,1))

        labels0 = {
            "x": "x-displacement (m)",
            "y": "y-displacement (m)",
            "alt": "Altitude - displacement (m)",
            "range": "Range - displacement (m)",
            "t": "Mission time (s)",
            "dx": "x - velocity (m/s)",
            "dy": "y - velocity (m/s)",
            "dxy": "Magnitude velocity (m/s)",
            "t": "Mission time (s)",
            "heading": "Heading (deg)",
            "ang": "Vehicle direction (deg)",
            "t": "Mission time (s)"
        }

        bgfix = {
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            }

        df = rocket.get_log()
        # print(df)

        def make_fig(x,y,title,text,col):
            fig = px.line(df, x=x, y=y, template=template, title=title,
                           labels=labels0)
            fig.update_layout(bgfix)
            col.plotly_chart(fig, use_container_width=True)
            col.markdown(text)

        text0 = 'Range is the displacement following the surface of the earth, altitude is the distance above the surface of the earth.'
        make_fig("range","alt","Downrange distance and Altitude",text0,col1)

        text1 = 'Same information as above but split into alt and range; plotted against mission time.'
        make_fig("t",["alt", "range"],"Altitude and range displacements.",text1,col1)

        text10 = 'alt,range and magnitude velocity against mission time.'
        make_fig("t",["dalt", "drange", "dxy"],"X and y displacements against time in the cartesian grid",text10,col1)


        text2 = 'This graph shows the same information as on the left but in an absolute cartesian form. Useful for seeing how the rocket flies around the curvuture of the earth.'
        make_fig("x","y","x and y displacements in the cartesian grid",text2,col2)

        text3 = 'Same info as above, split into compnents '
        make_fig("t",["y","x"],"x and y displacements in the cartesian grid",text3,col2)

        text3 = 'x,y and magnitude velocity against mission time.'
        make_fig("t",["dy", "dx", "dxy"],"X and y displacements against time in the cartesian grid",text3,col2)

        text4=''
        make_fig("t",["heading","ang"],"Heading (in the absolute cartesian grid)",text4,col2)


        text5='Fuel and total vehicle mass'
        make_fig("t",["fuel","mass"],"Heading (in the absolute cartesian grid)",text5,col1)






if __name__ == '__main__':
    main()
