from graphparse.dockerfile_gen.Demand_solvers.solve_interface import SolveInterface
from graphparse.neo4j_reader.neo4j_reader import Neo4jConnection


# 2.输入镜像名和版本号，根据文件系统包推荐软件包
class SolverType2(SolveInterface):
    def type_solver(self) -> str:
        content = ""
        image_name = self.demand.image_name
        image_version = self.demand.image_version
        entity_node_list = []
        with Neo4jConnection() as conn:
            # 通过镜像名和镜像版本获取镜像结点
            image_node = conn.get_image_node_by_image_name_and_version(image_name, image_version)
            if image_node is None:
                return content
            entity_node_list.append(image_node)
            # 根据基础镜像获取文件系统包
            file_pkg_node = conn.get_file_pkg_by_base_image(image_node.hash_value)
            # 通过文件系统包结点寻找所有依赖结点和配置结点
            if file_pkg_node:
                entity_node_list.append(file_pkg_node)
                # 寻找所有依赖结点
                dependency_node_list = conn.get_dependency_node_list_of_file_pkg(file_pkg_node.hash_value)
                entity_node_list.extend(dependency_node_list)
                # 寻找所有配置结点
                config_node_list = conn.get_config_node_list_of_file_pkg(file_pkg_node.hash_value)
                entity_node_list.extend(config_node_list)

        for entity_node in entity_node_list:
            content += entity_node.pretty() + "\n"

        return content
