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
import scipy.constants as ctes
from dataclasses import dataclass, field
from typing import Literal

type Vector2d = np.ndarray[tuple[Literal[2]], np.dtype[np.float64]]

@dataclass
class SimulationData:
    _mass: float = 0.0
    _vol_total: float = 0.0
    _vol_displaced: float = 0.0
    _dist: Vector2d = field(default_factory=lambda: np.zeros((2,)))
    _velocity: Vector2d = field(default_factory=lambda: np.zeros((2,)))

    def potential_energy(self) -> float:
        """Potential energy, mass X gravity (weight) X height."""
        return self._mass * ctes.g * self._dist[1]

    def kinetic_energy(self) -> float:
        """Kinetic energy, mass X velocity squared, halved."""
        return self._mass * self._velocity.dot(self._velocity)/2.0

    # --------------------------------------------------------------------------
    # Getters and setters
    # --------------------------------------------------------------------------

    @property
    def mass(self) -> float:
        return self._mass

    def density(self) -> float:
        return self._mass / self._vol_total

    @property
    def vol_total(self) -> float:
        return self._vol_total

    @property
    def vol_displaced(self) -> float:
        return self._vol_displaced

    @property
    def dist(self) -> Vector2d:
        return self._dist

    @property
    def velocity(self) -> Vector2d:
        return self._velocity

    @mass.setter
    def mass(self, new_mass: float) -> None:
        assert new_mass > 0.0
        self._mass = new_mass

    @vol_total.setter
    def vol_total(self, new_vol_total: float) -> None:
        assert new_vol_total > 0.0
        self._vol_total = new_vol_total

    @vol_displaced.setter
    def vol_displaced(self, new_vol_displaced: float) -> None:
        assert new_vol_displaced > 0.0
        self._vol_displaced = new_vol_displaced

    @dist.setter
    def dist(self, new_dist: Vector2d) -> None:
        assert len(new_dist) == 2
        self._dist = new_dist

    @velocity.setter
    def velocity(self, new_velocity: Vector2d) -> None:
        assert len(new_velocity) == 2
        self._velocity = new_velocity

    def __str__(self):
        str = f'Mass = {self._mass}\n'
        str += f'Volume = {self._vol_total}'
        return str

### -- simulation_data.py ------------------------------------------------------
