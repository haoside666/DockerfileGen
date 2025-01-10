from graphparse.dockerfile_gen.demand_solver.solve_interface import SolveInterface


# 2.输入镜像名和版本号，根据文件系统包推荐软件包
class SolverType2(SolveInterface):
    def type_solver(self) -> str:
        pass
