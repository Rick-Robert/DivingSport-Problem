# Introduction
    This document is intended to give an overview of the code, explaining briefly each implementation choice and highlighting the central classes and methods.
    No specific software architecture or design pattern was adopted, as it is a low-complexity project at the code level. 
    This implementation is based on the physics involving the practice of the diving sport, which is deeply discussed in the counterpart article. 
    The goal is to simulate the fall of an object through different mediums, intending to know its final position and velocity given a set of initial values.
# Implementation
## Classes

### **DiveAbstract**
    An abstract class that enables higher flexibility in the code, since any classes inherited from it can instantiate an object that can be used in the diving sports simulation, allowing the modeling of the physical bodies of different properties.
##### **Constructor** \_\_init\_\_(self) : 
    As an abstract class it is not possible to instantiate an object, therefore, the constructor has no use for this class, but its concrete subclasses can use it when instantiating. Also calls fix_density().

### **Setters**
**set_all**(self, mass:float, dist:np.array, vol_total:float, vol_dived:float, velocity: np.array): Method that calls other setters to redefine the values of all DiveAbstract's properties. Also calls **fix_density**().

**set_abstract**(self, abs_obj:"DiveAbstract"): Used to copy the inherit properties between concrete subclasses.

**set_mass**(self, mass: float): Redefine mass value. Also calls **fix_density**().

**set_dist**(self, dist: np.array): Redefine distance array.

**set_dist_x**(self, x: float): Redefine x component of distance.

**set_dist_y**(self, y: float): Redefine y component of distance.

**set_vol_total**(self, vol_total: float): Redefine total volume value. Also calls **fix_density**().

**set_vol_dived**(self, vol_dived: float): Redefine dived volume value.

**set_velocity**(self, velocity:np.array): Redefine velocity array.

**set_velocity_x**(self, x: float): Redefine x component of velocity.

**set_velocity_y**(self, y: float): Redefine y component of velocity.

**set_density**(self, density: float): Redefine density value.

**fix_density**(self): Considering homogeneous density, redefines based on mass and total volume of the object.

### **Getters**
**get_mass**(self) -> float: Get the mass value.

**get_dist**(self) -> np.array: Get copy of dist array.

**get_dist_x**(self) -> float: Get x component of distance.

**get_dist_y**(self) -> float: Get y component of distance.

**get_vol_total**(self) -> float: Get total volume value.

**get_vol_dived**(self) -> float: Get dived volume value.

**get_velocity**(self) -> np.array: Get copy of velocity array.

**get_velocity_x**(self) -> float: Get x component of velocity.

**get_velocity_y**(self) -> float: Get y component of velocity.

**get_density**(self) -> float: Get density value.

### **Calculate energies**
**gravitational_e**(self) -> float: Calculates the gravitational energy of an object based on its properties and the constant G.

**kinetic_e**(self) -> float: Calculates the kinetic energy of an object based on the magnitude of velocity.

**kinetic_e_x**(self) -> float: Calculates the kinetic energy of an object based on the x component of velocity.

**kinetic_e_y**(self) -> float: Calculates the kinetic energy of an object based on the y component of velocity.

**mechanical_e_y**(self) -> float: Sums the gravitational energy and kinetic energy.

### **Abstract methods**
**\_\_str\_\_**(self) -> str: What to return as a string when object is used inside **print()**.

**transv_volume**(self, length: float): Volume calculation based on transversal area, as the body will dive vertically (following the gravity direction) in a medium, one of the ways to calculate the displaced liquid's volume is to estimate the volume of the body when entering the liquid. That is, **transv_volume** is a concrete method that is different for every body shape and orientation.
### **DiveEllipsoid**
