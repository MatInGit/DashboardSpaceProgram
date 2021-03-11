import time

import streamlit as st
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sim import World, Vehicle


earth = World()
rocket = Vehicle()
rocket.place_on_surface(earth)

i = 0
dt = 0.1

x = []
y = []
dy =[]
dx = []
t_arr= []
t = 0
rocket.theta = 40

thrust = 1
# rocket.y = earth.radius+ 300000
# rocket.dy = 11000
while(i<160000):

    rocket.step(thrust,earth,dt)
    t_arr.append(t)
    x.append(rocket.x)
    y.append(rocket.y-earth.radius)
    dy.append(rocket.dy)
    dx.append(rocket.dx)

    wx,wy = earth.get_location()
    rx,ry = rocket.get_location()

    distance = np.sqrt((wx-rx)**2+(wy-ry)**2)

    # if distance-earth.radius> 25000:
    #     rocket.theta  = 10
    #     thrust = 0.5
    # if distance-earth.radius> 40000:
    #     rocket.theta  = 15
    #     thrust = 0.5
    # if distance-earth.radius> 70000:
    #     rocket.theta  = 25
    #     thrust = 0.3

    t+=dt
    i+=1


    if distance < earth.radius:
        break

# plt.plot(t_arr,dy)
# plt.plot(t_arr,dx)
# plt.plot(t_arr,y)
# plt.plot(t_arr,x)
##plt.plot(t_arr,np.sqrt(np.power(y, 2)+np.power(x, 2)))
# plt.plot(t_arr,dy)
plt.plot(earth.rho)
plt.show()
