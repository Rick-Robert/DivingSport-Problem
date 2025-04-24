import math
G = float(9.80665)
class dive_prism():
    def __init__(self, mass : float = 1, l_o: float | None = None, 
                 dist: float | None = None, t_area: float | None = None, vol_t: float | None = None, 
                 vol_disp: float = 0, vel_v: float = 0):
        #check if value is allowed
        if mass <= 0:
            print("Mass not positive, initializing as 1kg")
            mass = 1
        if l_o is not None and l_o <= 0:
            print("Length not positive, initializing as 1m")
            l_o = 1
        if t_area is not None and t_area <= 0:
            print("Transversal area not positive, initializing as 1m^2")
            t_area = 1
        if vol_t is not None and vol_t <= 0:
            print("Total volume not positive, initializing as 1m^3")
            vol_t = 1
        if vol_disp < 0:
            print("Displaced liquid's volume negative, initializing as 1m^3")
            vol_disp = 1
        
        #if two between t_area, l_o and vol_t is missing, calculate it
        if t_area is not None and l_o is not None:
            self.__mass = mass
            self.__l_o = l_o
            self.__dist = dist
            self.__t_area = t_area
            if vol_t is None:
                self.__vol_t = l_o*t_area
            else:
                self.__vol_t = vol_t
            self.__vol_disp = vol_disp
            self.__vel_v = vel_v
        elif t_area is not None and vol_t is not None:
            self.__mass = mass
            if l_o is None:
                self.__l_o = vol_t/t_area
            else:
                self.__l_o = l_o
            self.__dist = dist
            self.__t_area = t_area
            self.__vol_t = vol_t
            self.__vol_disp = vol_disp
            self.__vel_v = vel_v
        elif l_o is not None and vol_t is not None:
            self.__mass = mass
            self.__l_o = l_o
            self.__dist = dist
            if t_area is None:
                self.__t_area = vol_t/l_o
            else:
                self.__t_area = t_area
            self.__vol_t = vol_t
            self.__vol_disp = vol_disp
            self.__vel_v = vel_v
        else:
            raise ValueError("Must provide at least two between: l_o, t_area and vol_t")
    
    def __str__(self) -> str:
        return (f"Dive Prism:\nMass = {self.__mass}kg\nLength = {self.__l_o}m\nDistance from liquid's surface = {self.__dist}m\n"+
                f"Transversal Area = {self.__t_area}m^2\nTotal Volume = {self.__vol_t}m^3\n"+
                f"Displaced liquid's Volume = {self.__vol_disp}m^3\nVertical Velocity = {self.__vel_v}m/s"
        )
    #setters
    def set_mass(self, mass: float): ...
    def set_l_o(self, l_o: float): ...
    def set_dist(self, dist: float): ...
    def set_t_area(self, t_area:float): ...
    def set_vol_t(self, vol_t: float): ...
    def set_vol_disp(self, vol_disp: float): ...
    def set_vel_v(self, vel_v: float): ...
    
    #getters
    def get_mass(self) -> float: ...
    def get_l_o(self) -> float: ...
    def get_dist(self) -> float: ...
    def get_t_area(self) -> float: ...
    def get_vol_t(self) -> float: ...
    def get_vol_disp(self) -> float: ...
    def get_vel_v(self) -> float: ...
    def get_density(self) -> float: ...

    #check if length, transversal area and volume have reasonable values
    def check_dimensions(self): ...

    #fix_something change the value of the something based on the related variables
    def fix_l_o(self): ...
    def fix_vol_t(self): ...
    def fix_t_area(self): ...

    #calculate energys
    def get_grav_e(self) -> float: ... #gravitational energy
    def get_cin_e(self) -> float: ... #cinetic energy
    def get_mec_e(self) -> float: ... #mecanical energy

    def set_mass(self, mass: float):
        if mass <= 0:
            print("Mass not positive, initializing as 1kg")
            mass = 1
        self.__mass = mass
    
    def set_l_o(self, l_o: float):
        if l_o <= 0:
            print("Length not positive, initializing as 1m")
            l_o = 1
        self.__l_o = l_o

    def set_dist(self, dist: float):
        self.__dist = dist

    def set_t_area(self, t_area:float):
        if t_area <= 0:
            print("Transversal area not positive, initializing as 1m^2")
            t_area = 1
        self.__t_area = t_area
    
    def set_vol_t(self, vol_t: float):
        if vol_t <= 0:
            print("Total volume not positive, initializing as 1m^3")
            vol_t = 1
        self.__vol_t = vol_t
    
    def set_vol_disp(self, vol_disp: float):
        if vol_disp < 0:
            print("Displaced liquid's volume negative, initializing as 1m^3")
            vol_disp = 1
        self.__vol_disp = vol_disp

    def set_vel_v(self, vel_v: float):
        self.__vel_v = vel_v


    def get_mass(self) -> float:
        return self.__mass
    def get_l_o(self) -> float:
        return self.__l_o
    def get_dist(self) -> float:
        return self.__dist
    def get_t_area(self) -> float:
        return self.__t_area
    def get_vol_t(self) -> float:
        return self.__vol_t
    def get_vol_disp(self) -> float:
        return self.__vol_disp
    def get_vel_v(self) -> float:
        return self.__vel_v
    def get_density(self) -> float:
        return self.__mass/self.__vol_t

    def check_dimensions(self):
        if(not math.isclose(self.__l_o*self.__t_area, self.__vol_t)):
            print("dimensions: wrong")
        else:
            print("dimensions: ok")

    def fix_l_o(self):
        self.__l_o = self.__vol_t/self.__t_area
        print(self)

    def fix_vol_t(self):
        self.__vol_t = self.__t_area*self.__l_o
        print(self)

    def fix_t_area(self):
        self.__t_area = self.__vol_t/self.__l_o
        print(self)

    def get_grav_e(self) -> float: 
        return self.__mass*G*self.__dist #mgh
    def get_cin_e(self) -> float: 
        return (self.__mass*self.__vel_v**2)/2
    def get_mec_e(self) -> float:
        return self.get_grav_e()+self.get_cin_e()
        