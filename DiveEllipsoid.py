from DiveAbstract import DiveAbstract
import numpy as np

class DiveEllipsoid(DiveAbstract):
    def __init__(self, mass:float = 1, dist:float  = 0, vol_total:float = 1, vol_dived:float = 0, velocity: np.array = np.array([0,0])):
        super().__init__()
        self.set_all(mass,dist,vol_total,vol_dived,velocity)
        self._a:float = 1 #x axis
        self._b:float = 1 #y axis
        self._c:float = 1 #z axis

    def __str__(self) -> str:
        return (f"Dive Ellipsoid:\nMass = {self._mass}kg\nLength = ({self._a},{self._b},{self._c})m\nLeast distance from liquid's surface = {self._dist}m\n"+
                f"Total Volume = {self._vol_total}m^3\n"+
                f"Displaced liquid's Volume = {self._vol_dived}m^3\nVelocity = {self._velocity}m/s"
        )

    #Volume of transversal section: useful when diving vertically in liquid
    def transv_volume(self, length: float): #length of dove part
        pass
