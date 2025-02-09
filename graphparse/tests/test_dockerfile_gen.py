import unittest

from graphparse.datatypes.demand import Demand
from graphparse.dockerfile_gen.demand_solver import dockerfile_generator


class TestDockerfileGen(unittest.TestCase):

    def test_demand_1(self):
        demand = Demand("ubuntu")
        dockerfile_str = dockerfile_generator(demand)
        print(dockerfile_str)

    def test_demand_2(self):
        demand = Demand("ubuntu", "latest")
        dockerfile_str = dockerfile_generator(demand)
        print(dockerfile_str)
