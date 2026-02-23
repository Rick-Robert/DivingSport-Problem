import sys
import copy
import numpy as np
from DiveAbstract import DiveAbstract
from DiveEllipsoid import DiveEllipsoid
from math import *

G = float(9.80665) #gravity's sense is positive
DELTA_T = sys.float_info.epsilon*1e+10 #the smallest difference between two representable floats * 10^10 (reduces precision, but also reduces computing time)
D_LQD = 1000 #Liquid's Density

#methods
def free_fall_dist(real_dive:DiveAbstract, dist:float, drag_coeff:float, d: float) -> DiveAbstract:...
def free_fall_time(real_dive:DiveAbstract, time:float, drag_coeff:float, d: float) -> DiveAbstract:...
def weight(dive:DiveAbstract)->float:...
def buoyancy(dive:DiveAbstract, d: float):...
def no_drag_resultant(dive:DiveAbstract, d: float):...
def auto_c0_linear_drag_velocity_y(real_dive:DiveAbstract, v0_y:float, t0:float, k:float, d: float, time:float)->float:...
def auto_c0_quadratic_drag_velocity_y(real_dive:DiveAbstract, v0_y:float, t0:float, D:float, medium_d: float, time:float):...

#calculate consts
def linear_initial_const_y(real_dive:DiveAbstract, v0_y:float, k:float, d: float, t0:float)->float:...
def quadratic_tanh_initial_const_y(real_dive:DiveAbstract, v0_y: float, D:float, medium_d:float, t0:float):...

#Calculate velocity with drag
def linear_drag_velocity_y(real_dive:DiveAbstract, k:float, d: float, time:float, c0:float)->float:...
def quadratic_drag_velocity_y(real_dive:DiveAbstract, D:float, medium_d: float, time:float, c0:float):...

#Calculate velocity of a falling object and update its related properties (velocity and position)

def free_fall_dist(real_dive:DiveAbstract, dist:float, D:float, k:float, medium_d: float) -> DiveAbstract: #return object properties based on final distance and initial values
    dive = copy.deepcopy(real_dive)
    #linear_lim >= 0
    linear_lim = 0 #limit velocity magnitude where the drag force starts to be proportional to v^2 (instead of v, v stands for velocity magnitude)
    if D <=0 or k <= 0:
        print("invalid drag coefficient")
        pass
    if medium_d <= 0:
        print("invalid medium density")
        pass
    if(np.isclose(dive.get_dist_y(),dist)): #object didn't change position
        pass
    elif (no_drag_resultant(dive, medium_d) >= 0 and dive.get_velocity_y() >= 0) and dist-dive.get_dist_y() < 0:
        print("forces and velocity don't go negative direction")
        pass
    elif (weight(dive)+buoyancy(dive, medium_d) <= 0 and dive.get_velocity_y() <= 0) and dist-dive.get_dist_y() > 0:
        print("forces and velocity don't go positive direction")
        pass
    vel = dive.get_velocity_y()
    time = 0
    c0 = 0
    #for loop
    if(np.abs(vel) >= linear_lim):
        quadratic_drag_velocity_y(dive,D,medium_d,time,c0)
    else:
        linear_drag_velocity_y(dive,k,medium_d,time,c0)

def free_fall_time(real_dive:DiveAbstract, time:float, drag_coeff:float, d: float) -> DiveAbstract: #return object properties based on time passed and initial values
    dive = copy.deepcopy(real_dive)
    vel = dive.get_velocity_y()
    if vel > 0:
        return dive
    elif vel == 0:
        return dive
    else:
        return dive

def weight(dive:DiveAbstract)->float:
    return dive.get_mass()*G

def buoyancy(dive:DiveAbstract, d: float):
    if d <= 0:
        print("invalid medium density")
        pass
    return -G*d*dive.get_vol_dived()

def no_drag_resultant(dive:DiveAbstract, d: float):
    return weight(dive)+buoyancy(dive,d)

def linear_initial_const_y(real_dive:DiveAbstract, v0_y:float, k:float, d: float, t0:float)->float:
    return (v0_y-(G*(real_dive.get_mass()-d*real_dive.get_vol_dived()))/k)*np.exp(k*t0/real_dive.get_mass())

def auto_c0_linear_drag_velocity_y(real_dive:DiveAbstract, v0_y:float, t0:float, k:float, d: float, time:float)->float:
    c0 = linear_initial_const_y(real_dive, v0_y, k, d, t0)
    return (G*(real_dive.get_mass()-d*real_dive.get_vol_dived()))/k+c0/np.exp(k*time/real_dive.get_mass())

def linear_drag_velocity_y(real_dive:DiveAbstract, k:float, d: float, time:float, c0:float)->float: #would be slow to calculate c0 every time, e.g. in a loop
    return (G*(real_dive.get_mass()-d*real_dive.get_vol_dived()))/k+c0/np.exp(k*time/real_dive.get_mass())

def quadratic_tanh_initial_const_y(real_dive:DiveAbstract, v0_y: float, D:float, medium_d:float, t0:float):
    a = no_drag_resultant(real_dive,medium_d)
    if(not np.isclose(a,0)):
        if(np.sign(a) == np.sign(real_dive.get_velocity_y())):
            return np.arctanh(v0_y*np.sqrt(D/np.abs(a)))-np.sign(a)*np.sqrt(np.abs(a)*D)*t0/real_dive.get_mass() 
        else:
            return np.arctan(v0_y*np.sqrt(D/np.abs(a)))-np.sign(a)*np.sqrt(np.abs(a)*D)*t0/real_dive.get_mass()
    else:
        return (np.sign(v0_y)*real_dive.get_mass()-v0_y*D*t0)/v0_y

def auto_c0_quadratic_drag_velocity_y(real_dive:DiveAbstract, v0_y:float, t0:float, D:float, medium_d: float, time:float):
    a = no_drag_resultant(real_dive,medium_d)
    c0 = 0
    if(not np.isclose(a,0)): 
        if(np.sign(a) == np.sign(real_dive.get_velocity_y())):
            c0 = np.arctanh(v0_y*np.sqrt(D/np.abs(a)))-np.sign(a)*np.sqrt(np.abs(a)*D)*t0/real_dive.get_mass()
            return np.sqrt(np.abs(a)/D)*np.tanh(np.sign(a)*np.sqrt(np.abs(a)*D)*time/real_dive.get_mass()+c0)
        else:
            c0 = np.arctan(v0_y*np.sqrt(D/np.abs(a)))-np.sign(a)*np.sqrt(np.abs(a)*D)*t0/real_dive.get_mass()
            np.sqrt(np.abs(a)/D)*np.tan(np.sign(a)*np.sqrt(np.abs(a)*D)*time/real_dive.get_mass()+c0)
    else:
        c0 = (np.sign(v0_y)*real_dive.get_mass()-v0_y*D*t0)/v0_y
        return np.sign(real_dive.get_velocity_y())*real_dive.get_mass()/(D*time+c0)

def quadratic_drag_velocity_y(real_dive:DiveAbstract, D:float, medium_d: float, time:float, c0:float):
    a = no_drag_resultant(real_dive,medium_d)
    if(not np.isclose(a,0)):
        if(np.sign(a) == np.sign(real_dive.get_velocity_y())):
            return np.sqrt(np.abs(a)/D)*np.tanh(np.sign(a)*np.sqrt(np.abs(a)*D)*time/real_dive.get_mass()+c0)
        else:
            return np.sqrt(np.abs(a)/D)*np.tan(np.sign(a)*np.sqrt(np.abs(a)*D)*time/real_dive.get_mass()+c0)
    else:
        return np.sign(real_dive.get_velocity_y())*real_dive.get_mass()/(D*time+c0)

def no_velocity_y(real_dive:DiveAbstract, d:float, v0_y:float, t0:float, time:float): #only usable in a very small time where v == 0
    a = no_drag_resultant(real_dive,d)
    return a*time/real_dive.get_mass() + v0_y-a*t0/real_dive.get_mass()





    
