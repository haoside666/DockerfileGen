import unittest

from graphparse.datatypes.demand import Demand
from graphparse.dockerfile_gen.demand_solver import dockerfile_generator


class TestDockerfileGen(unittest.TestCase):

    def test_demand_1(self):
        demand = Demand("python")
        dockerfile_str = dockerfile_generator(demand)
        print(dockerfile_str)

    def test_demand_2(self):
        demand = Demand("python", "latest")
        dockerfile_str = dockerfile_generator(demand)
        print(dockerfile_str)

    def test_demand_3_pkg(self):
        demand = Demand(software_list=['pandas', 'requests'])
        dockerfile_str = dockerfile_generator(demand)
        print(dockerfile_str)

    def test_demand_3_tool_pkg(self):
        demand = Demand(software_list=['hdf5', 'go:1.8'])
        dockerfile_str = dockerfile_generator(demand)
        print(dockerfile_str)

    def test_demand_3_mix(self):
        demand = Demand(software_list=['pandas', 'requests', 'hdf5'])
        dockerfile_str = dockerfile_generator(demand)
        print(dockerfile_str)
