from graphgen.graph.Entity.EntityNode import EntityNode


class ExecutableNode(EntityNode):
    NodeName = 'ExeCmd'

    def __init__(self, cmd_name: str, cmd_type: str = "general") -> None:
        self.cmd_name: str = cmd_name
        self.cmd_type: str = cmd_type

    def pretty(self) -> str:
        return ""
