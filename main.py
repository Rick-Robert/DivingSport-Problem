from dive_prism import dive_prism
from math import *
import sys
G = float(9.80665)
DELTA_T = sys.float_info.epsilon*1e+10 #he smallest difference between two representable floats
D_LQD = 1000 #Liquid's Density

#calculate velocity of a falling object on new_dist, and updates dive_obj dist and vel_v
def calc_fall_vel(dive_obj: dive_prism, new_dist: float) -> float: ... 
def calc_entrance_vel(dive_obj: dive_prism, delta_t: float = DELTA_T) -> float: ...

#Air
def calc_fall_vel(dive_obj: dive_prism, new_dist: float) -> float:
    new_vel = sqrt(2*G*(dive_obj.get_dist()-new_dist) + dive_obj.get_vel_v()**2)
    dive_obj.set_vel_v(-new_vel)
    dive_obj.set_dist(new_dist)
    return new_vel

#Entrance
def calc_entrance_vel(dive_obj: dive_prism, delta_t: float = DELTA_T) -> float:
    vol_i = dive_obj.get_vol_disp()
    vol_t = dive_obj.get_vol_t()
    vol_ip1 = vol_i
    print(dive_obj.get_vel_v())
    while True:
        vel_im1 = dive_obj.get_vel_v()
        vol_ip1 = vol_i - dive_obj.get_t_area()*vel_im1*delta_t #quantity of volume of liquid displaced
        if vol_ip1 <= vol_i or vol_ip1 >= vol_t:
            break
        new_vel = vel_im1+((D_LQD*vol_ip1*G-dive_obj.get_mass()*G)/dive_obj.get_mass())*delta_t
        dive_obj.set_vel_v(new_vel)
        vol_i = vol_ip1
        dive_obj.set_vol_disp(vol_i)
    print(dive_obj.get_vel_v())
    return dive_obj.get_vel_v()
    

#Dive
#create an object
"""
mass, l_o, dist, t_area, vol_t, vol_disp, vel_v.
"""
dive_obj1 = dive_prism(75,1.7,10,0.3,None,0,0)
calc_fall_vel(dive_obj1, 0)
calc_entrance_vel(dive_obj1)
print(dive_obj1)
