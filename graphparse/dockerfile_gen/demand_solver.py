# 用户需求包括：
# 1.基础镜像及其版本
# 2.软件包(包括系统包和工具包)
from graphparse.datatypes.demand import Demand
from graphparse.dockerfile_gen.demand_solver.SolverType1 import SolverType1
from graphparse.dockerfile_gen.demand_solver.SolverType2 import SolverType2
from graphparse.dockerfile_gen.demand_solver.SolverType3 import SolverType3
from graphparse.dockerfile_gen.demand_solver.SolverType4 import SolverType4
from graphparse.dockerfile_gen.demand_solver.SolverType5 import SolverType5

# 1.只输入镜像名，不输入版本号，根据镜像权重推荐镜像版本，并根据文件系统包推荐软件包
# 2.输入镜像名和版本号，根据文件系统包推荐软件包
# 3.只输入软件包名
#   优先查找系统包，然后查找工具包
#   对于系统包，利用深度优先搜索，寻找所有依赖的软件包，
#   对于工具包，根据软件包权重推荐软件包版本，然后在根据软件包需求命令列表筛选满足需求命令且最优的镜像
# 4.输入镜像名和软件包名，不输入版本号
#   优先查找系统包，然后查找工具包
#   对于系统包，利用深度优先搜索，寻找所有依赖的软件包以及安装方式，根据镜像命令约束，选择最合适的安装方式
#   对于工具包，要求满足独一性约束，命令约束，然后根据软件包权重推荐最优软件包版本
# 5.输入镜像名和版本号和软件包名
#   优先查找系统包，然后查找工具包
#   对于系统包，利用深度优先搜索，寻找所有依赖的软件包以及安装方式，根据镜像命令约束，选择最合适的安装方式
#   对于工具包，要求满足独一性约束，命令约束，然后根据软件包权重推荐最优软件包版本

DICT_DEMAND_TYPE_SOLVE_MODULE_MAPPER = {
    1: SolverType1,
    2: SolverType2,
    3: SolverType3,
    4: SolverType4,
    5: SolverType5,
}


# 输入用户需求，生成Dockerfile
def dockerfile_generator(demand: Demand) -> str:
    demand_type = demand.get_demand_type()
    # 得到实体生成类
    solver_class = DICT_DEMAND_TYPE_SOLVE_MODULE_MAPPER[demand_type]
    solver_object = solver_class(demand)
    return solver_object.type_solver()
