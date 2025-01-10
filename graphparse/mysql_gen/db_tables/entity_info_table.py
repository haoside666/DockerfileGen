class Entity:
    def __init__(self, name=None, flags=None, value=None, label_name=None,
                 version=None, cmd_flag_list=None, cmd_operand_list=None, method=None,
                 url=None, cmd_list=None, cmd_type=None, pkg_list=None, version_list=None,
                 src=None, dest=None, types=None):
        self.name = name
        self.flags = flags
        self.value = value
        self.label_name = label_name
        self.version = version
        self.cmd_flag_list = cmd_flag_list
        self.cmd_operand_list = cmd_operand_list
        self.method = method
        self.url = url
        self.cmd_list = cmd_list
        self.cmd_type = cmd_type
        self.pkg_list = pkg_list
        self.version_list = version_list
        self.src = src
        self.dest = dest
        self.types = types

    def __repr__(self):
        return (f"Entity(name={self.name}, flags={self.flags}, value={self.value}, "
                f"label_name={self.label_name}, version={self.version}, cmd_flag_list={self.cmd_flag_list}, "
                f"cmd_operand_list={self.cmd_operand_list}, method={self.method}, url={self.url}, "
                f"cmd_list={self.cmd_list}, cmd_type={self.cmd_type}, pkg_list={self.pkg_list}, "
                f"version_list={self.version_list}, src={self.src}, dest={self.dest}, types={self.types})")