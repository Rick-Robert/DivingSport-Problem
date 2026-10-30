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
from dataclasses import dataclass, field

@dataclass
class SimulationData:
    _mass: float = 0.0
    _density: float = 0.0
    _vol_total: float = 0.0
    _vol_displaced: float = 0.0
    _dist: np.ndarray = field(default_factory=lambda: np.zeros(2))
    _velocity: np.ndarray = field(default_factory=lambda: np.zeros(2))

    @property
    def mass(self) -> float:
        return self._mass

    @property
    def density(self) -> float:
        return self._density

    @property
    def vol_total(self) -> float:
        return self._vol_total

    @property
    def vol_displaced(self) -> float:
        return self._vol_displaced

    @property
    def dist(self) -> np.ndarray:
        return self._dist

    @property
    def velocity(self) -> np.ndarray:
        return self._velocity

    @mass.setter
    def mass(self, new_mass: float) -> None:
        self._mass = new_mass

    @density.setter
    def density(self, new_density: float) -> None:
        self._density = new_density

    @vol_total.setter
    def vol_total(self, new_vol_total: float) -> None:
        self._vol_total = new_vol_total

    @vol_displaced.setter
    def vol_displaced(self, new_vol_displaced: float) -> None:
        self._vol_displaced = new_vol_displaced

    @dist.setter
    def dist(self, new_dist: np.ndarray) -> None:
        assert len(new_dist) == 2
        self._dist = new_dist

    @velocity.setter
    def velocity(self, new_velocity: np.ndarray) -> None:
        assert len(new_velocity) == 2
        self._velocity = new_velocity

### -- simulation_data.py ------------------------------------------------------
