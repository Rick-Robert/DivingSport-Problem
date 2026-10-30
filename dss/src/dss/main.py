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

import logging
import numpy as np
from simulation_data import SimulationData

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)5s] %(filename)s: (%(funcName)s) -> %(message)s",
)

logger = logging.getLogger(__name__)


def say_hello() -> None:
    """Simple 'Hello, World!' message."""
    logger.info('Starting DSS')

def say_goodbye() -> None:
    """Simple 'Hello, World!' message."""
    logger.info('Shuting down DSS')

def main() -> None:
    say_hello()

    sd = SimulationData()
    sd.mass = 1.39
    sd.density = 2.39
    sd.vol_total = sd.mass * sd.density
    sd.dist = np.full(2, 3.0)
    sd.velocity = np.array([1.0, 2.0])

    logger.info(sd)

    say_goodbye()

if __name__ == '__main__':
    main()

### -- main.py -----------------------------------------------------------------
