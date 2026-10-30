### ----------------------------------------------------------------------------
### ╺┳┓┏━┓┏━┓
###  ┃┃┗━┓┗━┓
### ╺┻┛┗━┛┗━┛
###
### This file is part of DSS - Diving Simulation Suit.
###
### by Rick Robert Tomaz Rezende <rick.rezende@estudante.ufscar.br>
###    Renato Cantão <rfcantao@ufscar.br>
### ----------------------------------------------------------------------------

import numpy as np
from dataclasses import dataclass

@dataclass
class DiveBase:
    _mass: float
    _density: float
    _vol_total: float
    _vol_displaced: float
    _dist: np.ndarray = np.array([0.0, 0.0])
    _velocity: np.ndarray = np.array([0.0, 0.0])

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, new_mass: float) -> None:
        self._mass = new_mass

### -- divebase.py -------------------------------------------------------------
