import sys
import copy
import numpy as np
from DiveAbstract import DiveAbstract
from DiveEllipsoid import DiveEllipsoid
from math import *
import time

G = float(9.80665) #gravity's sense is positive
DELTA_T = sys.float_info.epsilon*1e+10 #the smallest difference between two representable floats * 10^10 (reduces precision, but also reduces computing time)
D_LQD = 1000 #Liquid's Density

#methods
'''
def iterative_uniform_medium_dist(real_dive:DiveAbstract, dist:float, drag_coeff:float, d: float) -> DiveAbstract:...
def iterative_uniform_medium_time(real_dive:DiveAbstract,t0:float, time:float, D:float, k:float, medium_d: float) -> DiveAbstract:...
def weight(dive:DiveAbstract)->float:...
def buoyancy(dive:DiveAbstract, d: float):...
def no_drag_resultant(dive:DiveAbstract, d: float):...
def auto_c0_linear_drag_velocity_y(real_dive:DiveAbstract, v0_y:float, t0:float, k:float, d: float, time:float)->float:...
def auto_c0_quadratic_drag_velocity_y(real_dive:DiveAbstract, v0_y:float, t0:float, D:float, medium_d: float, time:float):...

#calculate consts
def linear_initial_const_vel_y(real_dive:DiveAbstract, v0_y:float, k:float, d: float, t0:float)->float:...
def quadratic_tanh_initial_const_y(real_dive:DiveAbstract, v0_y: float, D:float, medium_d:float, t0:float):...

#Calculate velocity with drag
def linear_drag_velocity_y(real_dive:DiveAbstract, k:float, d: float, time:float, c0:float)->float:...
def quadratic_drag_velocity_y(real_dive:DiveAbstract, D:float, medium_d: float, time:float, c0:float):...

#Calculate velocity of a falling object and update its related properties (velocity and position)'''

def iterative_uniform_medium_dist(real_dive:DiveAbstract, dist:float, D:float, k:float, medium_d: float) -> DiveAbstract: #return object properties based on final distance and initial values
    dive = copy.deepcopy(real_dive)
    no_drag_force = no_drag_resultant(dive, medium_d)
    distance_y = dist-dive.get_dist_y()
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
    elif (no_drag_force >= 0 and dive.get_velocity_y() >= 0) and distance_y < 0:
        print("forces and velocity don't go negative direction")
        pass
    elif (no_drag_force <= 0 and dive.get_velocity_y() <= 0) and distance_y > 0:
        print("forces and velocity don't go positive direction")
        pass
    time = 0
    steps_limit :int = 1e10
    steps :int= 0
    c0 :float= 0
    was_linear:bool=None
    #for loop
    #loop until
    #   body in desired dist
    #   limit of steps
    #   no acceleration in the desired sense and velocity contrary or zero
    vel = dive.get_velocity_y()
    curr_dist_y = dive.get_dist_y()
    while (steps < steps_limit) and (not np.isclose(dive.get_dist_y(),dist)):
        if(int(steps%1e5) == 0):
            print(f"time: {time}\nsteps: {steps}\n"+ ("Linear: " if was_linear else "Quadratic: "+str(c0))+"\n"+"="*20+"\n")
        curr_dist_y = curr_dist_y + vel*DELTA_T
        dive.set_dist_y(curr_dist_y)
        distance_y = dist-dive.get_dist_y()
        if(np.abs(vel) < linear_lim):
            dive_vel_y  = dive.get_velocity_y()
            if(np.isclose(no_drag_force+k*dive_vel_y, 0) and np.sign(dive_vel_y) != np.sign(distance_y)): #no acceleration, velocity doesn't go in sense of distance_y
                print("didnt add up linear")
                break
            if((was_linear is None) or was_linear is False): #calculates c0 only if it is the first time, or if it based on quadratic (beggining of a linear drag)
                was_linear = True
                c0 = linear_initial_const_vel_y(dive, vel, k, medium_d, time)
            vel = linear_drag_velocity_y(dive,k,medium_d,time,c0)
        else:
            dive_vel_y  = dive.get_velocity_y()
            if(np.isclose(no_drag_force+np.sign(dive_vel_y)*D*(dive_vel_y**2), 0) and np.sign(dive_vel_y) != np.sign(distance_y)): #no acceleration, velocity doesn't go in sense of distance_y
                print("didnt add up quadratic")
                break
            if((was_linear is None) or was_linear is True): 
                was_linear = False
                c0 = quadratic_initial_const_vel_y(dive, vel,D,medium_d,time)
            vel = quadratic_drag_velocity_y(dive,D,medium_d,time,c0)
        if(np.sign(distance_y) != np.sign(dist-(curr_dist_y + vel*DELTA_T))):
            print("After point, returning")
            break
        dive.set_velocity_y(vel)
        steps = steps + 1
        time = time + DELTA_T
        if(int(steps%1e5) == 0):
            print(dive)
        if(steps >= steps_limit):
            print("Steps limit")
        if(np.isclose(dive.get_dist_y(),dist)):
            print("Close call")
    print(dive)
    return dive

def iterative_uniform_medium_time(real_dive:DiveAbstract,t0:float, time:float, D:float, k:float, medium_d: float, linear_limit: float) -> DiveAbstract: #return object properties based on time passed and initial values
    dive = copy.deepcopy(real_dive)
    no_drag_force = no_drag_resultant(dive, medium_d)

    #linear_lim >= 0
    linear_lim = linear_limit #limit velocity magnitude where the drag force starts to be proportional to v^2 (instead of v, v stands for velocity magnitude)
    if D <=0 or k <= 0:
        print("invalid drag coefficient")
        pass
    if medium_d <= 0:
        print("invalid medium density")
        pass
    curr_time = t0
    steps_limit :int = 1e10
    steps :int= 0
    c0 :float= 0
    was_linear:bool=None
    #for loop
    #loop until
    #   body in desired dist
    #   limit of steps
    #   no acceleration in the desired sense and velocity contrary or zero
    vel = dive.get_velocity_y()
    curr_dist_y = dive.get_dist_y()
    while (steps < steps_limit) and (not np.isclose(curr_time,time)):
        time_diff = time-curr_time
        if(int(steps%1e5) == 0):
            print(f"time: {curr_time}\nsteps: {steps}\n"+ ("Linear: " if was_linear else "Quadratic: "+str(c0))+"\n"+"="*20+"\n")
        curr_dist_y = curr_dist_y + vel*DELTA_T
        dive.set_dist_y(curr_dist_y)
        if(np.abs(vel) < linear_lim):
            if((was_linear is None) or was_linear is False): #calculates c0 only if it is the first time, or if it based on quadratic (beggining of a linear drag)
                was_linear = True
                c0 = linear_initial_const_vel_y(dive, vel, k, medium_d, curr_time)
            vel = linear_drag_velocity_y(dive,k,medium_d,curr_time,c0)
        else:
            if((was_linear is None) or was_linear is True): 
                was_linear = False
                c0 = quadratic_initial_const_vel_y(dive, vel,D,medium_d,curr_time)
            vel = quadratic_drag_velocity_y(dive,D,medium_d,curr_time,c0)
        if(np.sign(time_diff) != np.sign(time-(curr_time + DELTA_T))):
            print("After point, returning")
            break
        dive.set_velocity_y(vel)
        steps = steps + 1
        curr_time = curr_time + DELTA_T
        if(int(steps%1e5) == 0):
            print(dive)
        if(steps >= steps_limit):
            print("Steps limit")
        if(np.isclose(curr_time,time)):
            print(f"Close call")
    print(dive)

def weight(dive:DiveAbstract)->float:
    return dive.get_mass()*G

def buoyancy(dive:DiveAbstract, d: float):
    if d <= 0:
        print("invalid medium density")
        pass
    return -G*d*dive.get_vol_dived()

def no_drag_resultant(dive:DiveAbstract, d: float):
    return weight(dive)+buoyancy(dive,d)

def linear_initial_const_vel_y(real_dive:DiveAbstract, v0_y:float, k:float, d: float, t0:float)->float:
    return (v0_y-(G*(real_dive.get_mass()-d*real_dive.get_vol_dived()))/k)*np.exp(k*t0/real_dive.get_mass())

def auto_c0_linear_drag_velocity_y(real_dive:DiveAbstract, v0_y:float, t0:float, k:float, d: float, time:float)->float:
    c0 = linear_initial_const_vel_y(real_dive, v0_y, k, d, t0)
    return (G*(real_dive.get_mass()-d*real_dive.get_vol_dived()))/k+c0/np.exp(k*time/real_dive.get_mass())

def linear_drag_velocity_y(real_dive:DiveAbstract, k:float, d: float, time:float, c0:float)->float: #would be slow to calculate c0 every time, e.g. in a loop
    return (G*(real_dive.get_mass()-d*real_dive.get_vol_dived()))/k+c0/np.exp(k*time/real_dive.get_mass())

def quadratic_initial_const_vel_y(real_dive:DiveAbstract, v0_y: float, D:float, medium_d:float, t0:float)->float:
    a = no_drag_resultant(real_dive,medium_d)
    if(not np.isclose(a,0)):
        if(np.sign(a) == np.sign(real_dive.get_velocity_y())):
            return np.arctanh(v0_y*np.sqrt(D/np.abs(a)))-np.sign(a)*np.sqrt(np.abs(a)*D)*t0/real_dive.get_mass() #returns c1/2, which was transformed when changing to tanh
        else:
            return np.arctan(v0_y*np.sqrt(D/np.abs(a)))-np.sign(a)*np.sqrt(np.abs(a)*D)*t0/real_dive.get_mass()
    else:
        return (np.sign(v0_y)*real_dive.get_mass()-v0_y*D*t0)/v0_y

def auto_c0_quadratic_drag_velocity_y(real_dive:DiveAbstract, v0_y:float, t0:float, D:float, medium_d: float, time:float)->float:
    a = no_drag_resultant(real_dive,medium_d)
    c0 = 0
    if(not np.isclose(a,0)): 
        if(np.sign(real_dive.get_velocity_y()) == 0 or np.sign(a) == np.sign(real_dive.get_velocity_y())):
            #print("arctanh")
            c0 = np.arctanh(v0_y*np.sqrt(D/np.abs(a)))-np.sign(a)*np.sqrt(np.abs(a)*D)*t0/real_dive.get_mass()
            return np.sqrt(np.abs(a)/D)*np.tanh(np.sign(a)*np.sqrt(np.abs(a)*D)*time/real_dive.get_mass()+c0)
        else:
            #print("arctan")
            c0 = np.arctan(v0_y*np.sqrt(D/np.abs(a)))-np.sign(a)*np.sqrt(np.abs(a)*D)*t0/real_dive.get_mass()
            return np.sqrt(np.abs(a)/D)*np.tan(np.sign(a)*np.sqrt(np.abs(a)*D)*time/real_dive.get_mass()+c0)
    else:
        #print("1/time")
        c0 = (np.sign(v0_y)*real_dive.get_mass()-v0_y*D*t0)/v0_y
        return np.sign(real_dive.get_velocity_y())*real_dive.get_mass()/(D*time+c0)

def quadratic_drag_velocity_y(real_dive:DiveAbstract, D:float, medium_d: float, time:float, c0:float)->float:
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

def conditional_uniform_medium_time(real_dive:DiveAbstract,t0:float, time:float, D:float, k:float, medium_d: float, linear_lim:float)->DiveAbstract: 
    dive = copy.deepcopy(real_dive)
    a = no_drag_resultant(real_dive,medium_d)
    q = linear_lim
    v0_y :float= real_dive.get_velocity_y()
    s0_y:float= real_dive.get_dist_y()
    if(v0_y == 0 or np.sign(a) == np.sign(v0_y)): #velocity's absolute value increases
        if np.abs(v0_y) < q: #velocity in linear range
            if(np.abs(a/k) >= q): #but can go to quadratic
                linear_lim_time = expected_linear_time(dive, v0_y, q, t0, k, medium_d)
                if time < linear_lim_time: #if time doens't go to quadratic
                    dive.set_velocity_y(auto_c0_linear_drag_velocity_y(dive,v0_y,t0,k,medium_d,time))
                    dive.set_dist_y(auto_c0_linear_drag_dist_y(dive,v0_y,t0,s0_y,t0,k,medium_d,time))
                else:
                    v0_y_past = v0_y
                    v0_y = auto_c0_linear_drag_velocity_y(dive,v0_y,t0,k,medium_d,linear_lim_time) #velocity at the end of q
                    s0_y = auto_c0_linear_drag_dist_y(dive,v0_y_past,t0,s0_y,t0,k,medium_d,linear_lim_time)
                    t0 = linear_lim_time
                    dive.set_velocity_y(auto_c0_quadratic_drag_velocity_y(dive,v0_y,t0,D,medium_d,time)) #the remainder time is in quadratic
                    dive.set_dist_y(auto_c0_quadratic_drag_dist_y(dive,v0_y,t0,s0_y,t0,D,medium_d,time))
            else:
                dive.set_velocity_y(auto_c0_linear_drag_velocity_y(dive,v0_y,t0,k,medium_d,time))
                dive.set_dist_y(auto_c0_linear_drag_dist_y(dive,v0_y,t0,s0_y,t0,k,medium_d,time))
        else:
            dive.set_velocity_y(auto_c0_quadratic_drag_velocity_y(dive,v0_y,t0,D,medium_d,time)) #only quadratic
            dive.set_dist_y(auto_c0_quadratic_drag_dist_y(dive,v0_y,t0,s0_y,t0,D,medium_d,time))
    else:
        if np.abs(v0_y) < q:
            if(np.abs(a/k) >= q):
                linear_lim_time = expected_linear_time(dive, v0_y, -np.sign(v0_y)*q, t0, k, medium_d) #time from v to q that velocity is going
                if time < linear_lim_time: #time reached before velocity goes to quadratic drag
                    dive.set_velocity_y(auto_c0_linear_drag_velocity_y(dive,v0_y,t0,k,medium_d,time))
                    dive.set_dist_y(auto_c0_linear_drag_dist_y(dive,v0_y,t0,s0_y,t0,k,medium_d,time))
                else:
                    v0_y_past = v0_y
                    v0_y = auto_c0_linear_drag_velocity_y(dive,v0_y,t0,k,medium_d,linear_lim_time) #velocity at the end of q
                    s0_y = auto_c0_linear_drag_dist_y(dive,v0_y_past,t0,s0_y,t0,k,medium_d,linear_lim_time)
                    t0 = linear_lim_time
                    dive.set_velocity_y(auto_c0_quadratic_drag_velocity_y(dive,v0_y,t0,D,medium_d,time)) #the remainder time is in quadratic
                    dive.set_dist_y(auto_c0_quadratic_drag_dist_y(dive,v0_y,t0,s0_y,t0,D,medium_d,time))
        else:
            quadratic_lim_time = expected_quadratic_time(dive, v0_y, np.sign(v0_y)*q, t0, D, medium_d) #time from v to q that velocity is going
            if time < quadratic_lim_time: #time reached before velocity goes to linear drag
                dive.set_velocity_y(auto_c0_quadratic_drag_velocity_y(dive,v0_y,t0,D,medium_d,time))
                dive.set_dist_y(auto_c0_quadratic_drag_dist_y(dive,v0_y,t0,s0_y,t0,D,medium_d,time))
            else:
                v0_y :float = auto_c0_quadratic_drag_velocity_y(dive,v0_y,t0,D,medium_d,quadratic_lim_time) #velocity at the beginning of linear drag
                t0 = quadratic_lim_time
                linear_lim_time = expected_linear_time(dive, v0_y, -np.sign(v0_y)*q, t0, k, medium_d) #time from v to q that velocity is going
                if time < linear_lim_time: #time reached before velocity goes to quadratic drag
                    dive.set_velocity_y(auto_c0_linear_drag_velocity_y(dive,v0_y,t0,k,medium_d,time))
                    dive.set_dist_y(auto_c0_linear_drag_dist_y(dive,v0_y,t0,s0_y,t0,k,medium_d,time))
                else:
                    v0_y_past = v0_y
                    v0_y = auto_c0_linear_drag_velocity_y(dive,v0_y,t0,k,medium_d,linear_lim_time) #velocity at the end of q
                    s0_y = auto_c0_linear_drag_dist_y(dive,v0_y_past,t0,s0_y,t0,k,medium_d,linear_lim_time)
                    t0 = linear_lim_time
                    dive.set_velocity_y(auto_c0_quadratic_drag_velocity_y(dive,v0_y,t0,D,medium_d,time)) #the remainder time is in quadratic
                    dive.set_dist_y(auto_c0_quadratic_drag_dist_y(dive,v0_y,t0,s0_y,t0,D,medium_d,time))
    return dive
                    


def expected_linear_time(real_dive:DiveAbstract, v0_y:float, vf_y:float, t0:float, k:float, medium_d: float) -> float:
    a = no_drag_resultant(real_dive,medium_d)
    lin_const = linear_initial_const_vel_y(real_dive,v0_y,k,medium_d,t0)#initial const
    return np.log((lin_const*k)/(k*vf_y-a))*real_dive.get_mass()/k #solves for time

def expected_quadratic_time(real_dive:DiveAbstract, v0_y:float, vf_y:float, t0:float, D:float, medium_d: float) -> float:
    a = no_drag_resultant(real_dive,medium_d)
    c0 = quadratic_initial_const_vel_y(real_dive,v0_y,D,medium_d,t0)
    if(not np.isclose(a,0)):
        if(np.sign(a) == np.sign(real_dive.get_velocity_y())):
            return (real_dive.get_mass()/np.sign(a)*np.sqrt(np.abs(a)*D))*(np.arctanh(vf_y*np.sqrt(D/np.abs(a)))-c0)
        else:
            return (real_dive.get_mass()/np.sign(a)*np.sqrt(np.abs(a)*D))*(np.arctan(vf_y*np.sqrt(D/np.abs(a)))-c0)
    else:
        return (real_dive.get_mass()*np.sign(v0_y)/vf_y-c0)/D
    
def linear_initial_const_dist_y(real_dive:DiveAbstract,v0_y:float, t0_v:float, s0_y:float, t0_s:float, k:float, d: float)->float:
    a = no_drag_resultant(real_dive, d)
    c0 = linear_initial_const_vel_y(real_dive, v0_y, k, d, t0_v)
    m = real_dive.get_mass()
    return s0_y-a/k*t0_s-m*a*c0/(k*k*np.e**(k*t0_s/m))

def auto_c0_linear_drag_dist_y(real_dive:DiveAbstract,v0_y:float, t0_v:float, s0_y:float, t0_s:float, k:float, d: float, time:float)->float:
    print("auto_lin_dist")
    a = no_drag_resultant(real_dive, d)
    m = real_dive.get_mass()
    c0 = linear_initial_const_vel_y(real_dive, v0_y, k, d, t0_v)
    c1 = linear_initial_const_dist_y(real_dive,v0_y,t0_v,s0_y,t0_s,k,d)
    return a/k*time+m*a*c0/(k*k*np.e**(k*time/m))+c1

def linear_drag_dist_y(real_dive:DiveAbstract, k:float, d: float, time:float, c0:float, c1:float)->float: #would be slow to calculate c0 every time, e.g. in a loop
    a = no_drag_resultant(real_dive, d)
    m = real_dive.get_mass()
    return a/k*time+m*a*c0/(k*k*np.e**(k*time/m))+c1

def quadratic_initial_const_dist_y(real_dive:DiveAbstract, v0_y:float, t0_v:float, s0_y:float, t0_s:float, D:float, medium_d:float)->float:
    a = no_drag_resultant(real_dive,medium_d)
    m = real_dive.get_mass()
    c1 = quadratic_initial_const_vel_y(real_dive,v0_y,D,medium_d,t0_v)
    if(not np.isclose(a,0)):
        if(np.sign(a) == np.sign(real_dive.get_velocity_y())):
            c1 = c1*2 #returns to be the c1 before changing to tanh
            return s0_y-np.sign(a)*m/D*np.log(np.abs(np.e**((np.sign(a)*2*np.sqrt(np.abs(a)*D)*t0_s)/m+c1)+1))+np.sqrt(np.abs(a)/D)*t0_s
        else:
            return s0_y+np.sign(a)*m/D*np.log(np.abs(np.cos(np.sign(a)*np.sqrt(np.abs(a)*D)*t0_s/m+c1)))
    else:
        return  s0_y-np.sign(real_dive.get_velocity_y())*m/D*np.log(np.abs(D*t0_s+c1))
    
def auto_c0_quadratic_drag_dist_y(real_dive:DiveAbstract, v0_y:float, t0_v:float, s0_y:float, t0_s:float, D:float, medium_d: float, time:float)->float:
    print(f"auto_quad_dist\nv0_y: {v0_y}, t0_v: {t0_v}, s0_y: {s0_y}, t0_s: {t0_s}, D: {D}, medium_d: {medium_d}, time: {time}")
    
    a = no_drag_resultant(real_dive, medium_d)
    m = real_dive.get_mass()
    c0 = quadratic_initial_const_vel_y(real_dive, v0_y, D, medium_d, t0_v)
    c1 = quadratic_initial_const_dist_y(real_dive, v0_y, t0_v, s0_y, t0_s, D, medium_d)
    if(not np.isclose(a,0)): 
        if(np.sign(real_dive.get_velocity_y()) == 0 or np.sign(a) == np.sign(real_dive.get_velocity_y())):
            #print("arctanh")
            c0 = c0*2 #c0 is c0/2 because of translation to tanh
            print(f"a: {a}\nc0: {c0}\nc1: {c1}")
            return np.sign(a)*m/D*np.log(np.abs(np.e**((np.sign(a)*2*np.sqrt(np.abs(a)*D)*time)/m+c0)+1))-np.sqrt(np.abs(a)/D)*time+c1
        else:
            #print("arctan")
            return -np.sign(a)*m/D*np.log(np.abs(np.cos(np.sign(a)*np.sqrt(np.abs(a)*D)*time/m+c0)))+c1
    else:
        #print("1/time")
        np.sign(real_dive.get_velocity_y())*m/D*np.log(np.abs(D*time+c0))+c1

def quadratic_drag_dist_y(real_dive:DiveAbstract, D:float, medium_d: float, time:float, c0:float, c1:float)->float: #already corrects c0 to c0*2 when tanh case
    a = no_drag_resultant(real_dive, medium_d)
    m = real_dive.get_mass()
    if(not np.isclose(a,0)): 
        if(np.sign(real_dive.get_velocity_y()) == 0 or np.sign(a) == np.sign(real_dive.get_velocity_y())):
            #print("arctanh")
            c0 = c0*2 #c0 is c0/2 because of translation to tanh
            return np.sign(a)*m/D*np.sign(a)*m/D*np.log(np.abs(np.e**((np.sign(a)*2*np.sqrt(np.abs(a)*D)*time)/m+c0)+1))-np.sqrt(np.abs(a)/D)*time+c1
        else:
            #print("arctan")
            return -np.sign(a)*m/D*np.log(np.abs(np.cos(np.sign(a)*np.sqrt(np.abs(a)*D)*time/m+c0)))+c1
    else:
        #print("1/time")
        np.sign(real_dive.get_velocity_y())*m/D*np.log(np.abs(D*time+c0))+c1

start_time = time.perf_counter()

human = DiveEllipsoid(90,np.array([0,-1]),70,70,np.array([0,0]))
print(human)
print("="*30)
#iterative_uniform_medium_dist(human,0,2,1.3,1.2)
#iterative_uniform_medium_time(human,0,0.5,2,1.3,1.2,0)
guy = conditional_uniform_medium_time(human,0,1000,2,1.3,1.2,2)
print(guy)
end_time = time.perf_counter()
elapsed_time = end_time-start_time
print(f"Elapsed time: {elapsed_time}s")

    
