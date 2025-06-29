from graphgen.shell_parse.shasta.command_node import Command, CommandNode, PipeNode, AndNode, OrNode, SemiNode, IfNode, \
    SubshellNode, NotNode, RedirNode, BackgroundNode, DefunNode, ForNode, WhileNode, CaseNode, RedirectionNode, \
    FileRedirNode, DupRedirNode, HeredocRedirNode, AssignNode
from graphgen.shell_parse.shasta.char_type import ArgChar, AArgChar, BArgChar, CArgChar, EArgChar, QArgChar, TArgChar, VArgChar
from typing import List, Dict
from graphgen.config.definitions import TEMP_VAR_C_LIST_PATH, TEMP_B_TYPE_PATH
from graphgen.shell_parse.shasta.util import print_to_file


def to_ast_node(obj) -> Command:
    k, v = obj
    if k == CommandNode.NodeName:
        node = CommandNode(line_number=v[0],
                           assignments=to_assigns(v[1]),
                           arguments=to_args(v[2]),
                           redir_list=to_redirs(v[3]))
    elif k == PipeNode.NodeName:
        node = PipeNode(is_background=v[0],
                        items=to_ast_nodes(v[1]))
    elif k == AndNode.NodeName:
        node = AndNode(left_operand=to_ast_node(v[0]),
                       right_operand=to_ast_node(v[1]))
    elif k == OrNode.NodeName:
        node = OrNode(left_operand=to_ast_node(v[0]),
                      right_operand=to_ast_node(v[1]))
    elif k == SemiNode.NodeName:
        node = SemiNode(left_operand=to_ast_node(v[0]),
                        right_operand=to_ast_node(v[1]))
    elif k == IfNode.NodeName:
        node = IfNode(cond=to_ast_node(v[0]),
                      then_b=to_ast_node(v[1]),
                      else_b=to_ast_node(v[2]))
    elif k == SubshellNode.NodeName:
        node = SubshellNode(line_number=v[0],
                            body=to_ast_node(v[1]),
                            redir_list=to_redirs(v[2]))
    elif k == NotNode.NodeName:
        node = NotNode(body=to_ast_node(v))
    elif k == RedirNode.NodeName:
        node = RedirNode(line_number=v[0],
                         node=to_ast_node(v[1]),
                         redir_list=to_redirs(v[2]))
    elif k == BackgroundNode.NodeName:
        node = BackgroundNode(line_number=v[0],
                              node=to_ast_node(v[1]),
                              redir_list=to_redirs(v[2]))
    elif k == DefunNode.NodeName:
        node = DefunNode(line_number=v[0],
                         name=v[1],
                         body=to_ast_node(v[2]))
    elif k == ForNode.NodeName:
        node = ForNode(line_number=v[0],
                       argument=to_args(v[1]),
                       body=to_ast_node(v[2]),
                       variable=v[3])
    elif k == WhileNode.NodeName:
        node = WhileNode(test=to_ast_node(v[0]),
                         body=to_ast_node(v[1]))
    elif k == CaseNode.NodeName:
        node = CaseNode(line_number=v[0],
                        argument=to_arg(v[1]),
                        cases=to_case_list(v[2]))
    else:
        raise ValueError()
    return node


def to_ast_nodes(node_list):
    new_node_list = [to_ast_node(ast_node) for ast_node in node_list]
    return new_node_list


def to_assigns(assignments) -> List[AssignNode]:
    new_assignments = []
    for name, val in assignments:
        new_assignments.append(AssignNode(var=name,
                                          val=to_arg(val)))
    return new_assignments


def to_redirs(redir_list) -> List[RedirectionNode]:
    new_redir_list = [to_redir(redir) for redir in redir_list]
    return new_redir_list


def to_redir(redir) -> RedirectionNode:
    k, v = redir
    if k == "File":
        return FileRedirNode(redir_type=v[0],
                             fd=v[1],
                             arg=to_arg(v[2]))
    elif k == "Dup":
        return DupRedirNode(dup_type=v[0],
                            fd=v[1],
                            arg=to_arg(v[2]))
    elif k == "Heredoc":
        return HeredocRedirNode(heredoc_type=v[0],
                                fd=v[1],
                                arg=to_arg(v[2]))
    assert False


def to_args(arg_list) -> List[List[ArgChar]]:
    new_arg_list = [to_arg(arg) for arg in arg_list]
    return new_arg_list


## TODO: Make this return an Arg (since we have that class already)
def to_arg(arg_char_list) -> List[ArgChar]:
    new_arg_char_list = [to_arg_char(arg_char) for arg_char in arg_char_list]
    return new_arg_char_list


def to_arg_char(arg_char) -> ArgChar:
    k, v = arg_char
    if k == "C":
        return CArgChar(v)
    elif k == "E":
        return EArgChar(v)
    elif k == "T":
        return TArgChar(v)
    elif k == "A":
        return AArgChar(to_arg(v))
    elif k == "V":
        print_to_file(TEMP_VAR_C_LIST_PATH, v[2] + "\n")
        return VArgChar(fmt=v[0],
                        null=v[1],
                        var=v[2],
                        arg=to_arg(v[3]))
    elif k == "Q":
        return QArgChar(to_arg(v))
    elif k == "B":
        cmd: Command = to_ast_node(v)
        # print_to_file(TEMP_B_TYPE_PATH, cmd.feature().json())
        print_to_file(TEMP_B_TYPE_PATH, "含有``或$()形式")
        return BArgChar(cmd)
    assert False


def to_case_list(case_list) -> List[Dict]:
    new_case_list = [{'cpattern': to_args(case['cpattern']),
                      'cbody': to_ast_node(case['cbody'])}
                     for case in case_list]
    return new_case_list
