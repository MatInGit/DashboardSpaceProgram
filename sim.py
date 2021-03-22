import numpy as np
import pandas as pd
import math
import ast

class logger:

    def __init__(self):
        self.log = pd.DataFrame([])


class Master:
    def __init__(self):
        self.objects = []

    # add objects to scene
    def self_add_to_scene(self):
        pass

    # pass time for all objects in the scene
    def pass_time(self, dt):
        pass


class World:
    def __init__(self, config="Earth"):

        if config == "Earth":


            # properties
            self.mass = 5.972e24
            self.radius = 6371e3

            # location
            self.x = 0
            self.y = 0

            # atmosphere density profile taken from https://www.grc.nasa.gov/www/k-12/self/atmosmet.html
            self.bounday_altitude = 120
            self.rho = []

            for i in range(self.bounday_altitude):
                if i <= 11:
                    T = 15.04 - 0.00649*i*1000
                    p = 101.29*((T+273.1)/288.08)**5.256

                elif i > 11 and i <= 25:
                    T = -56.46
                    p = 22.65*np.exp(1.73-0.000157*i*1000)

                elif i > 25:
                    T = -131.21+0.00288*i*1000
                    p = 2.488*((T+273.1)/216.6)**-11.388

                rho = p/(.2869*(T+273.1))
                self.rho.append(rho)
                i += 1

            # print(self.rho)
            print("Earth config selected!")
        else:
            print("Unknown Config!")

        # get location of body

    def get_location(self):
        return self.x, self.y

        # calculate the acceleration at a given altitude
    def get_acc(self, distance):
        G = 6.67430e-11
        Acc = G*(self.mass/(distance)**2)
        return Acc

    # pass time - do nothing
    def step(self):
        pass

        # this is a simple version, should be interpolated
    def get_rho(self, distance):
        height = distance - self.radius

        index = self.find_nearest(self.rho, height/1000).astype("int")
        # print(height,index)
        # print(self.rho[index])
        return self.rho[index]


    def find_nearest(self, array, value):
        array = np.asarray(range(len(array)))
        idx = (np.abs(array - value)).argmin()
        return array[idx]


class Vehicle:
    def __init__(self, config="Basic"):

        self.data_log = []


        #commands
        self._thurst_state = np.zeros(10)
        self._angle_state = np.zeros(10)
        self.desired_thrust = 0
        self.desired_angle = 0

        self.radius = 3.7

        # metric tons
        self.start_mass = 549e3
        self.mass = 549e3
        self.init_fuel_mass = 440e3
        self.fuel_mass = 440e3

        # kilo-newtons
        self.thrust_sl = 8027e3# 7609e3
        self.thrust_vac = 8227e3
        self.thrust = 0

        # seconds
        self.burn_time = 162

        # other
        self.x = 0
        self.y = 0
        self.theta = 0

        self.dx = 0
        self.dy = 0

        self.accx = 0
        self.accy = 0
        self.acc_mag = 0

        self.world = None

        self.dtheta = 0

        self.drag_coeff = 0.3

        self.alt = 0
        self.range = 0

        self.dalt = 0
        self.drange = 0

        self.fuel_per_sec = self.fuel_mass/self.burn_time
        self.heading = 0
        self.t = 0

        self.separation = False

    def place_on_surface(self, world):

        radius = world.radius

        self.x = 0  # align with world centre
        self.y = radius  # place on surface
        self.theta = 0  # point upwards

    def get_location(self):
        return self.x, self.y

    def command_parser(self,command,world):

        res = ast.literal_eval(command)

        for rule in res.keys():

            statement_is_true = True
            for var in res[rule]["condition"].keys():

                for comparator in res[rule]["condition"][var].keys():

                    value = res[rule]["condition"][var][comparator]

                    if var == "t":
                        read_value = self.t
                    if var == "alt":
                        rx, ry = self.get_location()
                        wx, wy = world.get_location()
                        read_value = np.sqrt((wx-rx)**2+(wy-ry)**2)- world.radius
                    if var == "range":
                        rx, ry = self.get_location()
                        read_value = np.arctan2((rx), (ry))*world.radius
                    if var == "heading":
                        read_value = self.heading
                    if var == "dalt":
                        read_value = self.dalt
                    if var == "drange":
                        read_value = self.drange

                    if comparator == ">":
                        if not (read_value > value):
                            statement_is_true = False
                            break
                    if comparator == ">=":
                        if not (read_value >= value):
                            statement_is_true = False
                            break
                    if comparator == "<":
                        if not (read_value < value):
                            statement_is_true = False
                            break
                    if comparator == "<=":
                        if not (read_value <= value):
                            statement_is_true = False
                            break
                    if comparator == "==":
                        if not (read_value == value):
                            statement_is_true = False
                            break

            if statement_is_true:
                for action in res[rule]["action"].keys():
                    if action == "thrust":
                        self.desired_thrust = np.clip(res[rule]["action"][action],0,1)

                    if action == "angle":
                        if type(res[rule]["action"][action]) == type(str(1)):
                            if res[rule]["action"][action] == "prograde":
                                self.desired_angle = np.degrees(self.heading)
                            if res[rule]["action"][action] == "retrograde":
                                self.desired_angle = np.degrees(self.heading - np.pi)
                        else:
                            self.desired_angle = res[rule]["action"][action]
                    if action == "separation":
                        if not self.separation:
                            self.separation = True
                            self.mass -= 97e3
                            print(self.mass)
                    if action == "griself.data_logins":
                        if not self.separation:
                            if res[rule]["action"][action] == "fold":
                                self.drag_coeff = 0.3
                            if res[rule]["action"][action] == "deploy":
                                self.drag_coeff = 1.3
    def get_log(self):
        cols = ["t","x","y","dx","dy","dxy","alt","range","dalt","drange","heading","ang","mass","fuel"]
        return pd.DataFrame(self.data_log,columns = cols)


    def log_data(self):
        array_log = []
        array_log.append(self.t)
        array_log.append(self.x)
        array_log.append(self.y- self.world.radius)
        array_log.append(self.dx)
        array_log.append(self.dy)
        array_log.append(np.sqrt(np.power(self.dy, 2)+np.power(self.dx, 2)))
        array_log.append(self.alt)
        array_log.append(self.range)
        array_log.append(self.dalt)
        array_log.append(self.drange)
        array_log.append(np.degrees(self.heading))
        array_log.append(self.theta)
        array_log.append(self.mass)
        array_log.append(self.fuel_mass)

        self.data_log.append(array_log)

    def step(self, commands, world, dt,t = None):  # gonna add angle and commands
        self.world = world



        self.command_parser(commands,world)

        # if type(commands)== type({"d":0}):
        #     for i in commands.keys():
        #         if i == "thrust":
        #              self.desired_thrust = commands[i]
        #         if i == "theta":
        #             self.desired_angle= commands[i]

        self._thurst_state[0] = self.thrust
        self.thrust =  self.thrust + (self.desired_thrust-self.thrust)/2
        self.theta =  self.theta + (self.desired_angle-self.theta)/40
        # print(self.theta, self.desired_angle)



        if self.fuel_mass < 0:
            self.thrust = 0



        wx, wy = world.get_location()
        diffx = -wx + self.x
        diffy = -wy + self.y
        distance = np.sqrt(np.power(diffx,2)+np.power(diffy,2))
        cogang = np.arctan2(diffx,diffy)


        grav_acc = (-world.get_acc(distance))


        grav_accx = grav_acc*np.sin(cogang)
        grav_accy = grav_acc*np.cos(cogang)


        self.heading = np.arctan2(self.dx,self.dy)

        drag_acc = (self.drag_coeff *((world.get_rho(distance)*np.sqrt(self.dx**2+self.dy**2)**2)/2)*(np.pi*self.radius**2))/self.mass
        drag_accx = -drag_acc * np.sin(self.heading)
        drag_accy = -drag_acc * np.cos(self.heading)

        # print(acc_mag)

        self.acc_mag = ((self.thrust_sl*self.thrust)/self.mass)

        self.accx = self.acc_mag * np.sin(np.radians(self.theta))
        self.accy = self.acc_mag * np.cos(np.radians(self.theta))

        # print("Gravity")
        # print(grav_accx ,grav_accy,grav_acc)
        #
        # print("Thrust")
        # print(accx,accy,acc_mag)
        #
        # print("Drag")
        # print(drag_accx,drag_accy,drag_acc)
        #
        # print("Speed")
        # print(self.dx,self.dy,np.sqrt(self.dy**2+self.dx**2))


        ### absolute reference grid calc ###

        self.dx += (self.accx + grav_accx + drag_accx)*dt
        self.dy += (self.accy + grav_accy + drag_accy)*dt

        self.x += self.dx*dt
        self.y += self.dy*dt
        self.theta += self.dtheta

        ### alt and range calc ###

        wx, wy = world.get_location()
        rx, ry = self.get_location()
        alt_temp = np.sqrt((wx-rx)**2+(wy-ry)**2) - world.radius
        range_temp = np.arctan2((rx), (ry))*world.radius

        self.dalt = (alt_temp - self.alt)/dt
        self.drange = (range_temp - self.range)/dt

        self.alt = alt_temp
        self.range = range_temp

        self.mass -= self.thrust*self.fuel_per_sec*dt
        self.fuel_mass -= self.thrust*self.fuel_per_sec*dt
        self.t +=dt

        self.log_data()
