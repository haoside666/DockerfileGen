from enum import Enum


# 关系类型
class RType(Enum):
    Contain = "Contain"
    Compatible = "Compatible"
    Dependency = "Dependency"
    Has = "Has"
    Settings = "Settings"
