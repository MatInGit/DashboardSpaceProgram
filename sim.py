import numpy as np
import pandas as pd
import math

class World:
    def __init__(self,config = "Earth"):

        if config == "Earth":
            # properties
            self.mass = 5.972e24
            self.radius = 6371e3

            # location
            self.x = 0
            self.y = 0

            # atmosphere density profile taken from https://www.grc.nasa.gov/www/k-12/rocket/atmosmet.html
            self.bounday_altitude = 120
            self.rho = []

            for i in range(self.bounday_altitude):
                if i <= 11:
                    T = 15.04 - 0.00649*i*1000
                    p = 101.29*((T+273.1)/288.08)

                elif i > 11 and i <= 25:
                    T = -56.46
                    p = 22.65*np.exp(1.73-0.000157*i*1000)

                elif i > 25:
                    T = -131.21+0.00288*i*1000
                    p = 2.488*((T+273.1)/216.6)**-11.388

                rho = p/(.2869*(T+273.1))
                self.rho.append(rho)
                i+=1

            # print(self.rho)
            print("Earth config selected!")
        else:
            print("Unknown Config!")


        # get location of body
    def get_location(self):
        return self.x,self.y

        # calculate the acceleration at a given altitude
    def get_acc(self, distance):
        G = 6.67430e-11
        Acc = G*(self.mass/(distance)**2)
        return Acc

        # this is a simple version, should be interpolated
    def get_rho(self,distance):
        height = distance - self.radius
        index = int (self.find_nearest(self.rho, height/1000))
        return self.rho[index]

    def find_nearest(self,array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

class Vehicle:
    def __init__(self,config = "Basic"):

        # rocket parameters sorted by units

        self.radius = 3.7

        # metric tons
        self.start_mass = 549e3
        self.mass = 549e3
        self.fuel_mass = 440e3

        # kilo-newtons
        self.thrust_sl = 7609e3
        self.thrust_vac= 8227e3

        # seconds
        self.burn_time = 162

        #other
        self.x = 0
        self.y = 0
        self.theta = 0

        self.dx = 0
        self.dy = 0
        self.dtheta = 0

        self.drag_coeff = 0.7

        self.fuel_per_sec = self.fuel_mass/self.burn_time

    def place_on_surface(self,world):

        radius = world.radius

        self.x = 0              #  align with world centre
        self.y = radius         #  place on surface
        self.theta = 0          #  point upwards

    def step(self, thrust, world,dt): # gonna add angle and commands
        if self.mass < (self.start_mass - self.fuel_mass):
            thrust = 0

        self.x += self.dx*dt
        self.y += self.dy*dt

        wx,wy = world.get_location()
        diffx   = wx - self.x
        diffy   = wy - self.y
        distance = np.sqrt(diffx**2+diffy**2)

        drag_force = -self.drag_coeff*((world.get_rho(distance)*np.sqrt(self.dx**2+self.dy**2)**2)/2)*(np.pi*self.radius**2)

        grav_force = -world.get_acc(distance)*self.mass # this needs to be automatically applied to be directed towards the world
        # print(grav_force,drag_force,self.thrust_sl*thrust,grav_force+drag_force+self.thrust_sl*thrust)
        self.dx += 0
        self.dy += ((grav_force + drag_force + self.thrust_sl*thrust)/self.mass)*dt

        self.mass -= thrust*self.fuel_per_sec*dt
