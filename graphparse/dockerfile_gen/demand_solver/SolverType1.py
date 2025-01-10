from graphparse.dockerfile_gen.demand_solver.solve_interface import SolveInterface


# 1.只输入镜像名，不输入版本号，根据镜像权重推荐镜像版本，并根据文件系统包推荐软件包
class SolverType1(SolveInterface):
    def type_solver(self) -> str:
        pass
