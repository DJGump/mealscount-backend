from .naive import OneToOneCEPStrategy,OneGroupCEPStrategy
from .mc_algo_v2 import AlgoV2CEPStrategy
from .binning import BinCEPStrategy
from .exhaustive import ExhaustiveCEPStrategy
from .spread import SpreadCEPStrategy
from .pairs import PairsCEPStrategy
from .nyc_moda_simulated_annealing import NYCMODASimulatedAnnealingCEPStrategy

STRATEGIES = {
    "OneToOne":OneToOneCEPStrategy,
    "OneGroup":OneGroupCEPStrategy,
    "Binning":BinCEPStrategy,
    #"AlgoV2":AlgoV2CEPStrategy,
    "Exhaustive":ExhaustiveCEPStrategy,
    "Spread":SpreadCEPStrategy,
    "Pairs": PairsCEPStrategy,
    "NYCMODA": NYCMODASimulatedAnnealingCEPStrategy,
}

