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
dt = 0.05

x = []
y = []
dy =[]
dx = []
t_arr= []
t = 0
ang = []
rocket.theta = 0

thrust = 1
# rocket.y = earth.radius+ 200000
# rocket.dx = 10500
while(i<2*160000):

    rocket.step(thrust,earth,dt)
    t_arr.append(t)
    x.append(rocket.x)
    y.append(rocket.y-earth.radius)
    dy.append(rocket.dy)
    dx.append(rocket.dx)
    ang.append(rocket.theta)

    wx,wy = earth.get_location()
    rx,ry = rocket.get_location()

    distance = np.sqrt((wx-rx)**2+(wy-ry)**2)

    rocket.desired_angle = (1-np.exp(-t/160))*120

    if t > 140:
        thrust = 0
        rocket.drag_coeff = 0.8
    if t > 161 and t < 163:
        rocket.desired_angle = np.degrees(rocket.heading - np.pi)
        thrust = 1
    if distance-earth.radius < 1750 and t > 100:
        rocket.desired_angle = np.degrees(rocket.heading - np.pi)
        thrust = 1

    # if distance-earth.radius> 100000:
    #     rocket.theta  = 90
    #     thrust = 1
    # if distance-earth.radius> 140000:
    #     rocket.theta  = 90
    #     thrust = 1

    t+=dt
    i+=1


    if distance < earth.radius and t > 10:
        print("crash!")
        break
draw_circle = plt.Circle((0.0, 0.0-earth.radius), earth.radius,fill=False)

plt.gcf().gca().add_artist(draw_circle)
#
# # plt.plot(t_arr,y)
# plt.plot(x,y)
# plt.plot(t_arr,x)
# plt.plot(t_arr,y)
# plt.plot(t_arr,dx)
# plt.plot(t_arr,dy)
# plt.plot(t_arr,np.sqrt(np.power(dy, 2)+np.power(dx, 2)))
# plt.plot(t_arr,ang)
# plt.plot(t_arr,dy)
# plt.plot(earth.rho)
plt.show()
