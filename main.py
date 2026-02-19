import sys
import copy
from DiveAbstract import DiveAbstract
from DiveEllipsoid import DiveEllipsoid
from math import *

G = float(9.80665) #gravity's sense is positive
DELTA_T = sys.float_info.epsilon*1e+10 #the smallest difference between two representable floats * 10^10 (reduces precision, but also reduces computing time)
D_LQD = 1000 #Liquid's Density

#Calculate velocity of a falling object and update its related properties (velocity and position)

def free_fall_dist(real_dive:DiveAbstract, dist:float, drag_coeff:float, medium_density: float) -> DiveAbstract: #return object properties based on final distance and initial values
    dive = copy.deepcopy(real_dive)
    #linear_lim >= 0
    linear_lim = 0 #limit velocity magnitude where the drag force starts to be proportional to v^2 (instead of v, v stands for velocity magnitude)
    if drag_coeff <=0:
        print("invalid drag coefficient")
        pass
    if medium_density <= 0:
        print("invalid medium density")
        pass
    if(dive.get_dist_y() == dist): #object didn't change position
        pass
    elif (no_drag_resultant(dive, medium_density) >= 0 and dive.get_velocity_y() >= 0) and dist-dive.get_dist_y() < 0:
        print("forces and velocity don't go negative direction")
        pass
    elif (weight(dive)+buoyancy(dive,medium_density) <= 0 and dive.get_velocity_y() <= 0) and dist-dive.get_dist_y() > 0:
        print("forces and velocity don't go positive direction")
        pass
    vel = dive.get_velocity_y()
    '''if vel > 0 + linear_lim: #quadratic
        return dive
    elif vel > 0: #linear
        return dive
    elif vel == 0: #no drag
        return dive
    elif vel > 0 - linear_lim: #linear
        return dive
    else: #quadratic
        return dive'''
    if vel == 0:
        pass
    elif(no_drag_resultant(dive, medium_density) > 0):
        if vel > 0 + linear_lim: #quadratic
            return dive
        elif vel > 0: #linear
            return dive
        elif vel > 0 - linear_lim: #linear
            return dive
        else: #quadratic
            return dive
    elif(no_drag_resultant(dive, medium_density) < 0):
        if vel > 0 + linear_lim: #quadratic
            return dive
        elif vel > 0: #linear
            return dive
        elif vel > 0 - linear_lim: #linear
            return dive
        else: #quadratic
            return dive
    else: #no acceleration, except drag with there is velocity
        if vel > 0 + linear_lim: #quadratic
            return dive
        elif vel > 0: #linear
            return dive
        elif vel > 0 - linear_lim: #linear
            return dive
        else: #quadratic
            return dive
def free_fall_time(real_dive:DiveAbstract, time:float, drag_coeff:float, medium_density: float) -> DiveAbstract: #return object properties based on time passed and initial values
    dive = copy.deepcopy(real_dive)
    vel = dive.get_velocity_y()
    if vel > 0:
        return dive
    elif vel == 0:
        return dive
    else:
        return dive
    pass
def weight(dive:DiveAbstract)->float:
    return dive.get_mass()*G
def buoyancy(dive:DiveAbstract, medium_density: float):
    if medium_density <= 0:
        print("invalid medium density")
        pass
    return -G*medium_density*dive.get_vol_dived()
def no_drag_resultant(dive:DiveAbstract, medium_density: float):
    return weight(dive)+buoyancy(dive,medium_density)

