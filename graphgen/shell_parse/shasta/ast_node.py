from abc import abstractmethod, ABCMeta
from typing import List, Tuple
from graphgen.shell_parse.datatypes.PrimitiveFeatureList import PrimitiveFeatureList


class AstNode(metaclass=ABCMeta):
    NodeName = 'None'

    @abstractmethod
    def json(self) -> List:
        pass

    @abstractmethod
    def pretty(self) -> str:
        """
        Renders an AST back in shell syntax. 
        """
        pass


class Command(AstNode):
    @abstractmethod
    def feature(self) -> PrimitiveFeatureList:
        pass

    @staticmethod
    def get_redir_list_info(redir_list) -> Tuple[List[str], List[str], List[str]]:
        redir_input_list: List[str] = []
        redir_output_list: List[str] = []
        other_list: List[str] = []
        for item in redir_list:
            t, string = item.redir_feature()
            if t == 0:
                redir_input_list.append(string)
            elif t == 1:
                redir_output_list.append(string)
            elif t == 2:
                redir_input_list.append(string)
                redir_output_list.append(string)
            else:
                other_list.append(string)
        return redir_input_list, redir_output_list, other_list
