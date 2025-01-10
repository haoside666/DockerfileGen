# 用户需求包括：
# 1.基础镜像及其版本
# 2.软件包(包括系统包和工具包)


class Demand:
    def __init__(self, image_name="", image_version="", software_list=None):
        self.image_name = image_name
        self.image_version = image_version
        self.software_list = software_list

    # 需求类型包括：
    # 1.只输入镜像名，不输入版本号,不输入软件包
    # 2.输入镜像名和版本号,不输入软件包
    # 3.只输入软件包
    # 4.输入镜像名和软件包名，不输入版本号
    # 5.输入镜像名和版本号和软件包名
    def get_demand_type(self):
        if self.image_name != "" and self.image_version == "" and self.software_list is None:
            return 1
        elif self.image_name != "" and self.image_version != "" and self.software_list is None:
            return 2
        elif self.image_name == "" and self.image_version == "" and self.software_list is not None:
            return 3
        elif self.image_name != "" and self.image_version == "" and self.software_list is not None:
            return 4
        elif self.image_name != "" and self.image_version != "" and self.software_list is not None:
            return 5
