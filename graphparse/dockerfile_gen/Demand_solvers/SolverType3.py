from graphparse.dockerfile_gen.Demand_solvers.solve_interface import SolveInterface


# 3.只输入软件包名
#   优先查找系统包，然后查找工具包
#   对于系统包，利用深度优先搜索，寻找所有依赖的软件包，
#   对于工具包，根据软件包权重推荐软件包版本，然后在根据软件包需求命令列表筛选满足需求命令且最优的镜像
class SolverType3(SolveInterface):
    def type_solver(self) -> str:
        pass
