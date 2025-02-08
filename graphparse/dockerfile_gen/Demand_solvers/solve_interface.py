from abc import ABC, abstractmethod

from graphparse.datatypes.demand import Demand


class SolveInterface(ABC):
    def __init__(self, demand: Demand) -> None:
        self.demand: Demand = demand

    @abstractmethod
    def type_solver(self) -> str:
        pass
