from graphparse.dockerfile_gen.Demand_solvers.solve_interface import SolveInterface


# 4.输入镜像名和软件包名，不输入版本号
#   优先查找系统包，然后查找工具包
#   对于系统包，利用深度优先搜索，寻找所有依赖的软件包以及安装方式，根据镜像命令约束，选择最合适的安装方式
#   对于工具包，要求满足独一性约束，命令约束，然后根据软件包权重推荐最优软件包版本
class SolverType4(SolveInterface):
    def type_solver(self) -> str:
        pass
