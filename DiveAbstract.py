import math
import numpy as np
from abc import ABC, abstractmethod
G = float(9.80665)
class DiveAbstract(ABC):
    def __init__(self):
        self._mass: float = 2
        self._dist: np.ndarray = np.array([0, 0])
        self._vol_total: float | None = 1
        self._vol_dived: float = 0 #volume of liquid displaced
        self._velocity: np.ndarray = np.array([0, 0])
        self._density: float = 2
    #setters
    def set_all(self, mass:float, dist:np.array, vol_total:float, vol_dived:float, velocity: np.array):...
    def set_abstract(self, abs_obj:"DiveAbstract"):...
    def set_mass(self, mass: float): ...
    def set_dist(self, dist: np.array): ...
    def set_dist_x(self, x: float): ...
    def set_dist_y(self, y: float): ...
    def set_vol_total(self, vol_total: float): ...
    def set_vol_dived(self, vol_dived: float): ...
    def set_velocity(self, velocity:np.array): ...
    def set_velocity_x(self, x: float): ...
    def set_velocity_y(self, y: float): ...
    def set_density(self, density: float):...
    def fix_density(self):...
    
    #getters
    def get_mass(self) -> float: ...
    def get_dist(self) -> np.array: ...
    def get_dist_x(self) -> float: ...
    def get_dist_y(self) -> float: ...
    def get_vol_total(self) -> float: ...
    def get_vol_dived(self) -> float: ...
    def get_velocity(self) -> float: ... 
    def get_velocity_x(self) -> float: ...
    def get_velocity_y(self) -> float: ...
    def get_density(self) -> float: ...

    #calculate energys
    def get_grav_e(self) -> float: ... #gravitational energy
    def get_cin_e(self) -> float: ... #cinetic energy
    def get_mec_e(self) -> float: ... #mecanical energy

    #abstract
    @abstractmethod
    def __str__(self) -> str:...
    @abstractmethod
    def transv_volume(self, length: float):...

    def set_mass(self, mass: float):
        if mass <= 0:
            print("Mass not positive, initializing as 2kg")
            mass = 2
        self._mass = mass
        self.fix_density()

    def set_dist(self, dist: np.array):
        self._dist = np.copy(dist)
    def set_dist_x(self, x: float):
        self._dist[0] = x
    def set_dist_y(self, y: float):
        self._dist[1] = y

    def set_vol_total(self, vol_total: float):
        if vol_total <= 0:
            print("Total volume not positive, initializing as 1m^3")
            vol_total = 1
        self._vol_total = vol_total
        self.fix_density()
    
    def set_vol_dived(self, vol_dived: float):
        if vol_dived < 0:
            print("Displaced liquid's volume negative, initializing as 0m^3")
            vol_dived = 0
        self._vol_dived = vol_dived

    def set_velocity(self, velocity:np.array):
        self._velocity = np.copy(velocity)
    def set_velocity_x(self, x: float):
        self._velocity[0] = x
    def set_velocity_y(self, y: float):
        self._velocity[1] = y
    def set_density(self, density: float):
        if density <= 0:
            print("Density not positive, initializing as 2kg/m^3")
            density = 2
        self._density = density
    def set_all(self, mass:float, dist:np.array, vol_total:float, vol_dived:float, velocity: np.array):
        self.set_mass(mass)
        self.set_dist(dist)
        self.set_vol_total(vol_total)
        self.set_vol_dived(vol_dived)
        self.set_velocity(velocity)
        self.fix_density()
    def set_abstract(self, abs_obj: "DiveAbstract"):
        self._mass = abs_obj._mass
        self._dist = np.copy(abs_obj._dist)
        self._vol_total = abs_obj._vol_total
        self._vol_dived = abs_obj._vol_dived
        self._velocity = np.copy(abs_obj._velocity)
        self._density = abs_obj._density

    def get_mass(self) -> float:
        return self._mass
    def get_dist(self) -> np.array:
        return np.copy(self._dist)
    def get_dist_x(self) -> float:
        return self._dist[0]
    def get_dist_y(self) -> float:
        return self._dist[1]
    def get_vol_total(self) -> float:
        return self._vol_total
    def get_vol_dived(self) -> float:
        return self._vol_dived
    def get_velocity(self) -> np.array:
        return np.copy(self._velocity)
    def get_velocity_x(self) -> float:
        return self._velocity[0]
    def get_velocity_y(self) -> float:
        return self._velocity[1]
    def get_density(self) -> float:
        return self._density

    def gravitational_e(self) -> float: 
        return self._mass*G*self.get_dist_y() #mgh
    def kinetic_e(self) -> float: 
        return (self._mass*np.linalg.norm(self.get_velocity())**2)/2
    def kinetic_e_x(self) -> float: 
        return (self._mass*self.get_velocity_x()**2)/2
    def kinetic_e_y(self) -> float: 
        return (self._mass*self.get_velocity_y()**2)/2
    def mechanical_e_y(self) -> float:
        return self.gravitational_e()+self.kinetic_e_y()

    def fix_density(self):
        self.set_density(self.get_mass()/self.get_vol_total())

    @abstractmethod
    def __str__(self) -> str:
        pass

    #Volume of transversal section: useful when diving vertically in liquid
    @abstractmethod
    def transv_volume(self, length: float): #length of dove part
        pass

        