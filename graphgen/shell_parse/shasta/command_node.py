from json import JSONEncoder
from graphgen.shell_parse.shasta.ast_node import AstNode, Command
from graphgen.shell_parse.shasta.print_lib import *
from graphgen.shell_parse.shasta.char_type import ArgChar, string_of_arg
from graphgen.shell_parse.shasta.util import make_kv
from graphgen.shell_parse.datatypes.PrimitiveFeatureList import *
from typing import Tuple, Literal, Dict


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Command):
            return obj.json()
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)


class PipeNode(Command):
    NodeName = 'Pipe'
    is_background: bool
    items: List[Command]

    def __init__(self, is_background, items):
        self.is_background = is_background
        self.items = items

    def __repr__(self):
        if self.is_background:
            return "Background Pipe: {}".format(self.items)
        else:
            return "Pipe: {}".format(self.items)

    def json(self):
        json_output = make_kv(PipeNode.NodeName,
                              [self.is_background,
                               self.items])
        return json_output

    def pretty(self):
        bg = self.is_background
        ps = self.items
        p = intercalate(" | ", [item.pretty() for item in ps])

        if bg:
            return background(p)
        else:
            return p

    def feature(self) -> PrimitiveFeatureList:
        feat_list = [item.feature() for item in self.items]
        return get_pipe_primitive_feature_by_union_primitive_feature_list(feat_list)


class CommandNode(Command):
    NodeName = 'Command'
    line_number: int
    assignments: "List[AssignNode]"
    arguments: List[List[ArgChar]]
    redir_list: "List[RedirectionNode]"

    def __init__(self, line_number, assignments, arguments, redir_list):
        self.line_number = line_number
        self.assignments = assignments
        self.arguments = arguments
        self.redir_list = redir_list

    def __repr__(self):
        output = "Command: {}".format(self.arguments)
        if len(self.assignments) > 0:
            output += ", ass[{}]".format(self.assignments)
        if len(self.redir_list) > 0:
            output += ", reds[{}]".format(self.redir_list)
        return output

    def json(self):
        json_output = make_kv(CommandNode.NodeName,
                              [self.line_number,
                               self.assignments,
                               self.arguments,
                               self.redir_list])
        return json_output

    def pretty(self):
        assigns = self.assignments
        cmds = self.arguments
        redirs = self.redir_list

        str = " ".join([assign.pretty() for assign in assigns])
        if (len(assigns) == 0) or (len(cmds) == 0):
            pass
        else:
            str += " "
        str += separated(string_of_arg, cmds) + string_of_redirs(redirs)

        return str

    def feature(self) -> PrimitiveFeatureList:
        var_p_list: List[Tuple[str, str]] = []

        for item in self.assignments:
            var_p_list.append((item.var, item.get_var_string()))

        command: str = self.pretty()

        redir_input_list, redir_output_list, other_list = self.get_redir_list_info(self.redir_list)

        p_feat = PrimitiveFeature(var_p_list, command, redir_input_list, redir_output_list, other_list)
        return PrimitiveFeatureList([p_feat])


class SubshellNode(Command):
    NodeName = 'Subshell'
    line_number: int
    body: Command
    redir_list: "List[RedirectionNode]"

    def __init__(self, line_number, body, redir_list):
        self.line_number = line_number
        self.body = body
        self.redir_list = redir_list

    def __repr__(self):
        output = "Subshell: {}".format(self.body)
        if len(self.redir_list) > 0:
            output += ", reds[{}]".format(self.redir_list)
        return output

    def json(self):
        json_output = make_kv(SubshellNode.NodeName,
                              [self.line_number,
                               self.body,
                               self.redir_list])
        return json_output

    def pretty(self):
        return parens(self.body.pretty() + string_of_redirs(self.redir_list))

    def feature(self) -> PrimitiveFeatureList:
        feat: PrimitiveFeatureList = self.body.feature()
        feat.set_is_complex_flag()
        return feat


class AndNode(Command):
    NodeName = 'And'
    left_operand: Command
    right_operand: Command

    def __init__(self, left_operand, right_operand):
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __repr__(self):
        output = "{} && {}".format(self.left_operand, self.right_operand)
        return output

    def json(self):
        json_output = make_kv(AndNode.NodeName,
                              [self.left_operand,
                               self.right_operand])
        return json_output

    def pretty(self):
        return f'{braces(self.left_operand.pretty())} && {braces(self.right_operand.pretty())}'

    def feature(self) -> PrimitiveFeatureList:
        return union_primitive_feature(self.left_operand.feature(), self.right_operand.feature())


class OrNode(Command):
    NodeName = 'Or'
    left_operand: Command
    right_operand: Command

    def __init__(self, left_operand, right_operand):
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __repr__(self):
        output = "{} || {}".format(self.left_operand, self.right_operand)
        return output

    def json(self):
        json_output = make_kv(OrNode.NodeName,
                              [self.left_operand,
                               self.right_operand])
        return json_output

    def pretty(self):
        return f'{braces(self.left_operand.pretty())} || {braces(self.right_operand.pretty())}'

    def feature(self) -> PrimitiveFeatureList:
        return union_primitive_feature(self.left_operand.feature(), self.right_operand.feature())


class SemiNode(Command):
    NodeName = 'Semi'
    left_operand: Command
    right_operand: Command

    def __init__(self, left_operand, right_operand):
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __repr__(self):
        output = "{} ; {}".format(self.left_operand, self.right_operand)
        return output

    def json(self):
        json_output = make_kv(SemiNode.NodeName,
                              [self.left_operand,
                               self.right_operand])
        return json_output

    def pretty(self):
        return f'{braces(self.left_operand.pretty())},{braces(self.right_operand.pretty())}'

    def feature(self) -> PrimitiveFeatureList:
        return union_primitive_feature(self.left_operand.feature(), self.right_operand.feature())


class NotNode(Command):
    NodeName = 'Not'
    body: Command

    def __init__(self, body):
        self.body = body

    def __repr__(self):
        output = "! ".format(self.body)
        return output

    def json(self):
        json_output = make_kv(NotNode.NodeName,
                              self.body)
        return json_output

    def pretty(self):
        return f'! {braces(self.body.pretty())}'

    def feature(self) -> PrimitiveFeatureList:
        return self.body.feature()


class RedirNode(Command):
    NodeName = 'Redir'
    line_number: int
    node: Command
    redir_list: List

    def __init__(self, line_number, node, redir_list):
        self.line_number = line_number
        self.node = node
        self.redir_list = redir_list

    def __repr__(self):
        output = "Redir: {}".format(self.node)
        if len(self.redir_list) > 0:
            output += ", reds[{}]".format(self.redir_list)
        return output

    def json(self):
        json_output = make_kv(RedirNode.NodeName,
                              [self.line_number,
                               self.node,
                               self.redir_list])
        return json_output

    def pretty(self):
        return self.node.pretty() + string_of_redirs(self.redir_list)

    def feature(self) -> PrimitiveFeatureList:
        feat: PrimitiveFeatureList = self.node.feature()
        feat.set_is_complex_flag()
        return feat


class BackgroundNode(Command):
    NodeName = 'Background'
    line_number: int
    node: Command
    redir_list: List

    def __init__(self, line_number, node, redir_list):
        self.line_number = line_number
        self.node = node
        self.redir_list = redir_list

    def __repr__(self):
        output = "Background: {} &".format(self.node)
        if len(self.redir_list) > 0:
            output += ", reds[{}]".format(self.redir_list)
        return output

    def json(self):
        json_output = make_kv(BackgroundNode.NodeName,
                              [self.line_number,
                               self.node,
                               self.redir_list])
        return json_output

    def pretty(self):
        return background(self.node.pretty() + string_of_redirs(self.redir_list))

    def feature(self) -> PrimitiveFeatureList:
        feat: PrimitiveFeatureList = self.node.feature()
        feat.set_is_complex_flag()
        return feat


class DefunNode(Command):
    NodeName = 'Defun'
    line_number: int
    name: object
    body: Command

    def __init__(self, line_number, name, body):
        self.line_number = line_number
        self.name = name
        self.body = body

    def __repr__(self):
        output = "Defun: {} ".format(self.body)
        return output

    def json(self):
        json_output = make_kv(DefunNode.NodeName,
                              [self.line_number,
                               self.name,
                               self.body])
        return json_output

    def pretty(self):
        name = self.name
        body = self.body
        return name.__repr__() + "() {\n" + body.pretty() + "\n}"

    def feature(self) -> PrimitiveFeatureList:
        feat: PrimitiveFeatureList = self.body.feature()
        feat.set_is_complex_flag()
        return feat


class ForNode(Command):
    NodeName = 'For'
    line_number: int
    argument: List[List[ArgChar]]
    body: Command
    variable: object

    def __init__(self, line_number, argument, body, variable):
        self.line_number = line_number
        self.argument = argument
        self.body = body
        self.variable = variable

    def __repr__(self):
        output = "for {} in {}; do ({})".format(self.variable, self.argument, self.body)
        return output

    def json(self):
        json_output = make_kv(ForNode.NodeName,
                              [self.line_number,
                               self.argument,
                               self.body,
                               self.variable])
        return json_output

    def pretty(self):
        a = self.argument
        body = self.body
        var = self.variable
        return f'for {var} in {separated(string_of_arg, a)}; do {body.pretty()}; done'

    def feature(self) -> PrimitiveFeatureList:
        feat: PrimitiveFeatureList = self.body.feature()
        feat.set_is_complex_flag()
        return feat


class WhileNode(Command):
    NodeName = 'While'
    test: Command
    body: Command

    def __init__(self, test, body):
        self.test = test
        self.body = body

    def __repr__(self):
        output = "while {}; do {}; done".format(self.test, self.body)
        return output

    def json(self):
        json_output = make_kv(WhileNode.NodeName,
                              [self.test,
                               self.body])
        return json_output

    def pretty(self):
        first = self.test
        b = self.body

        if isinstance(first, NotNode):
            t = first.body
            return f'until {t.pretty()}; do {b.pretty()}; done '
        else:
            t = first
            return f'while {t.pretty()}; do {b.pretty()}; done '

    def feature(self) -> PrimitiveFeatureList:
        feat1: PrimitiveFeatureList = self.test.feature()
        feat2: PrimitiveFeatureList = self.body.feature()
        feat: PrimitiveFeatureList = union_primitive_feature(feat1, feat2)
        feat.set_is_complex_flag()
        return feat


class IfNode(Command):
    NodeName = 'If'
    cond: Command
    then_b: Command
    else_b: Command

    def __init__(self, cond, then_b, else_b):
        self.cond = cond
        self.then_b = then_b
        self.else_b = else_b

    def __repr__(self):
        c = self.cond
        t = self.then_b
        e = self.else_b
        output = "if {}; then {}".format(c, t)
        if is_empty_cmd(e):
            output += "; fi"
        elif isinstance(e, IfNode):
            output += f"; el{e}"
        else:
            output += f'; else {e}; fi'
        return output

    def json(self):
        json_output = make_kv(IfNode.NodeName,
                              [self.cond,
                               self.then_b,
                               self.else_b])
        return json_output

    def pretty(self):
        c = self.cond
        t = self.then_b
        e = self.else_b
        str1 = f'if {c.pretty()}; then {t.pretty()}'

        if is_empty_cmd(e):
            str1 += "; fi"
        elif isinstance(e, IfNode):
            str1 += "; el" + e.pretty()
        else:
            str1 += f'; else {e.pretty()}; fi'

        return str1

    def feature(self) -> PrimitiveFeatureList:
        feat1: PrimitiveFeatureList = self.cond.feature()
        feat2: PrimitiveFeatureList = self.then_b.feature()
        feat3: PrimitiveFeatureList = self.else_b.feature()
        feat: PrimitiveFeatureList = union_primitive_feature_list([feat1, feat2, feat3])
        feat.set_is_complex_flag()
        return feat


class CaseNode(Command):
    NodeName = 'Case'
    line_number: int
    argument: List[ArgChar]
    cases: List[Dict]

    # cases
    # {
    #   'cpattern': to_args(case['cpattern']), --->List[List[ArgChar]]
    #   'cbody': to_ast_node(case['cbody']) ,  --->Command
    # }
    def __init__(self, line_number, argument, cases):
        self.line_number = line_number
        self.argument = argument
        self.cases = cases

    def json(self):
        json_output = make_kv(CaseNode.NodeName,
                              [self.line_number,
                               self.argument,
                               self.cases])
        return json_output

    def pretty(self):
        a = self.argument
        cs = self.cases
        return f'case {string_of_arg(a)} in {separated(string_of_case, cs)} esac'

    def feature(self) -> PrimitiveFeatureList:
        feat_list: List[PrimitiveFeatureList] = []
        for case in self.cases:
            cmd: Command = case["cbody"]
            feat_list.append(cmd.feature())
        feat: PrimitiveFeatureList = union_primitive_feature_list(feat_list)
        feat.set_is_complex_flag()
        return feat


class AssignNode(AstNode):
    var: str
    val: List[ArgChar]

    def __init__(self, var: str, val):
        self.var = var
        self.val = val

    # TODO: Implement
    def __repr__(self):
        return f'{self.var}={self.val}'

    def json(self):
        json_output = [self.var, self.val]
        return json_output

    def pretty(self):
        return f'{self.var}={string_of_arg(self.val)}'

    def get_var_string(self) -> str:
        return string_of_arg(self.val)


class RedirectionNode(AstNode):
    redir_type: str
    fd: int
    arg: List[ArgChar]

    # 0 --> input
    # 1 --> output
    # 2 --> input and output
    # 3 --> other
    def redir_feature(self) -> Tuple[Literal[0, 1, 2, 3], str]:
        pass


class FileRedirNode(RedirectionNode):
    NodeName = "File"
    redir_type: str
    fd: int
    arg: List[ArgChar]

    def __init__(self, redir_type, fd, arg):
        self.redir_type = redir_type
        self.fd = fd
        self.arg = arg

    # TODO: Implement
    # def __repr__(self):
    #     return f''

    def json(self):
        json_output = make_kv(FileRedirNode.NodeName,
                              [self.redir_type,
                               self.fd,
                               self.arg])
        return json_output

    def pretty(self):
        subtype = self.redir_type
        fd = self.fd
        a = self.arg
        if subtype == "To":
            return show_unless(1, fd) + ">" + string_of_arg(a)
        elif subtype == "Clobber":
            return show_unless(1, fd) + ">|" + string_of_arg(a)
        elif subtype == "From":
            return show_unless(0, fd) + "<" + string_of_arg(a)
        elif subtype == "FromTo":
            return show_unless(0, fd) + "<>" + string_of_arg(a)
        elif subtype == "Append":
            return show_unless(1, fd) + ">>" + string_of_arg(a)
        assert False

    def redir_feature(self):
        if self.redir_type == "From":
            return 0, string_of_arg(self.arg)
        elif self.redir_type in ["To", "Clobber", "Append"]:
            return 1, string_of_arg(self.arg)
        elif self.redir_type == "FromTo":
            return 2, string_of_arg(self.arg)
        assert False


class DupRedirNode(RedirectionNode):
    NodeName = "Dup"
    dup_type: str
    fd: int
    arg: List[ArgChar]

    def __init__(self, dup_type, fd, arg):
        self.dup_type = dup_type
        self.fd = fd
        self.arg = arg

    # TODO: Implement
    # def __repr__(self):
    #     return f''

    def json(self):
        json_output = make_kv(DupRedirNode.NodeName,
                              [self.dup_type,
                               self.fd,
                               self.arg])
        return json_output

    def pretty(self):
        subtype = self.dup_type
        fd = self.fd
        tgt = self.arg
        if subtype == "ToFD":
            return show_unless(1, fd) + ">&" + string_of_arg(tgt)
        elif subtype == "FromFD":
            return show_unless(0, fd) + "<&" + string_of_arg(tgt)

    def redir_feature(self):
        if self.dup_type == "FromFD":
            return 0, string_of_arg(self.arg)
        elif self.dup_type in "ToFD":
            return 1, string_of_arg(self.arg)
        assert False


class HeredocRedirNode(RedirectionNode):
    NodeName = "Heredoc"
    heredoc_type: str
    fd: int
    arg: List[ArgChar]

    def __init__(self, heredoc_type, fd, arg):
        self.heredoc_type = heredoc_type
        self.fd = fd
        self.arg = arg

    # TODO: Implement
    # def __repr__(self):
    #     return f''

    def json(self):
        json_output = make_kv(HeredocRedirNode.NodeName,
                              [self.heredoc_type,
                               self.fd,
                               self.arg])
        return json_output

    def pretty(self):
        t = self.heredoc_type
        fd = self.fd
        a = self.arg
        heredoc = string_of_arg(a, quote_mode=HEREDOC)
        marker = fresh_marker0(heredoc)

        stri = show_unless(0, fd) + "<<"
        if t == "XHere":
            stri += marker
        else:
            stri += "'" + marker + "'"

        stri += "\n" + heredoc + marker + "\n"

        return stri

    def redir_feature(self):
        return 3, string_of_arg(self.arg, quote_mode=HEREDOC)


def string_of_case(c):
    pats = map(string_of_arg, c["cpattern"])

    return f'{intercalate("|", pats)}) {c["cbody"].pretty()};;'


def string_of_redirs(rs: List[RedirectionNode]):
    str = ""

    for redir in rs:
        str = str + " " + redir.pretty()

    return str


def ast_node_to_untyped_deep(node):
    if (isinstance(node, AstNode)):
        json_key, json_val = node.json()
        return [json_key, ast_node_to_untyped_deep(json_val)]
    elif (isinstance(node, list)):
        return [ast_node_to_untyped_deep(obj) for obj in node]
    elif (isinstance(node, tuple)):
        return [ast_node_to_untyped_deep(obj) for obj in node]
    elif (isinstance(node, dict)):
        return {k: ast_node_to_untyped_deep(v) for k, v in node.items()}
    else:
        return node


# def make_typed_semi_sequence(asts: list[Command]) -> Command | SemiNode:
#     assert (len(asts) > 0)
#
#     if len(asts) == 1:
#         return asts[0]
#     else:
#         acc = asts[-1]
#         ## Remove the last ast
#         iter_asts = asts[:-1]
#         for ast in iter_asts[::-1]:
#             acc = SemiNode(ast, acc)
#         return acc


def is_empty_cmd(e: Command):
    return isinstance(e, CommandNode) \
           and e.line_number == -1 \
           and len(e.assignments) == 0 \
           and len(e.arguments) == 0 \
           and len(e.redir_list) == 0


## Implements a pattern-matching style traversal over the AST
def ast_match(ast_node, cases, *args):
    return cases[type(ast_node).NodeName](*args)(ast_node)
