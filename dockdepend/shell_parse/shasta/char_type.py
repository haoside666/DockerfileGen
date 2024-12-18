from dockdepend.shell_parse.shasta.ast_node import AstNode, Command
from dockdepend.shell_parse.shasta.util import make_kv
from dockdepend.shell_parse.shasta.print_lib import UNQUOTED, QUOTED
from typing import List


class ArgChar(AstNode):
    ## This method formats an arg_char to a string to
    ## the best of its ability
    def format(self) -> str:
        raise NotImplementedError


# common character
class CArgChar(ArgChar):
    NodeName = 'C'
    char: int

    def __init__(self, char: int):
        self.char = char

    def __repr__(self):
        return self.format()

    def format(self) -> str:
        return chr(self.char)

    def json(self):
        json_output = make_kv(CArgChar.NodeName, self.char)
        return json_output

    def pretty(self, quote_mode=UNQUOTED) -> str:
        if quote_mode == QUOTED and chr(self.char) == '"':
            return '\\"'
        else:
            return chr(self.char)


# escape character
class EArgChar(ArgChar):
    NodeName = 'E'
    char: int

    def __init__(self, char: int):
        self.char = char

    def __repr__(self):
        return f'\\{chr(self.char)}'

    def format(self) -> str:
        ## TODO: This is not right. I think the main reason for the
        ## problems is the differences between bash and the posix
        ## standard.
        non_escape_chars = [92,  # \
                            61,  # =
                            91,  # [
                            93,  # ]
                            45,  # -
                            58,  # :
                            126,  # ~
                            42]  # *
        if self.char in non_escape_chars:
            return '{}'.format(chr(self.char))
        else:
            return '\\{}'.format(chr(self.char))

    def json(self):
        json_output = make_kv(EArgChar.NodeName, self.char)
        return json_output

    def pretty(self, quote_mode=UNQUOTED):
        param = self.char
        char = chr(param)

        ## MMG 2021-09-20 It might be safe to move everything except for " in the second list, but no need to do it if the tests pass
        ## '!' dropped for bash non-interactive bash compatibility
        ## Chars to escape unconditionally
        chars_to_escape = ["'", '"', '`', '(', ')', '{', '}', '$', '&', '|', ';']
        ## Chars to escape only when not quoted
        chars_to_escape_when_no_quotes = ['*', '?', '[', ']', '#', '<', '>', '~', ' ']
        if char in chars_to_escape:
            return '\\' + char
        elif char in chars_to_escape_when_no_quotes and quote_mode == UNQUOTED:
            return '\\' + char
        else:
            return escaped(param)


# special Characters ~
class TArgChar(ArgChar):
    NodeName = 'T'
    string: str

    def __init__(self, string: str):
        self.string = string

    def __repr__(self):
        return f''

    def format(self) -> str:
        pass

    def json(self):
        json_output = make_kv(TArgChar.NodeName, self.string)
        return json_output

    def pretty(self, quote_mode=UNQUOTED):
        param = self.string
        if param == "None":
            return "~"
        elif len(param) == 2:
            if param[0] == "Some":
                (_, u) = param

                return "~" + u
            else:
                assert False
        else:
            print("Unexpected param for T: %s" % param)


# arithmetic expansion operator (())
class AArgChar(ArgChar):
    NodeName = 'A'
    arg: List[ArgChar]

    def __init__(self, arg: List[ArgChar]):
        self.arg = arg

    # def __repr__(self):
    #     return f''

    def format(self) -> str:
        pass

    def json(self):
        json_output = make_kv(AArgChar.NodeName, self.arg)
        return json_output

    def pretty(self, quote_mode=UNQUOTED):
        param = self.arg
        return f'$(({string_of_arg(param, quote_mode)}))'


# variable type character
class VArgChar(ArgChar):
    NodeName = 'V'
    fmt: object
    null: bool
    var: str
    arg: List[ArgChar]

    def __init__(self, fmt, null: bool, var: str, arg: List[ArgChar]):
        self.fmt = fmt
        self.null = null
        self.var = var
        self.arg = arg

    def __repr__(self):
        return f'V({self.fmt},{self.null},{self.var},{self.arg})'

    def format(self) -> str:
        return '${{{}}}'.format(self.var)

    def json(self):
        json_output = make_kv(VArgChar.NodeName,
                              [self.fmt,
                               self.null,
                               self.var,
                               self.arg])
        return json_output

    def pretty(self, quote_mode=UNQUOTED):
        vt = self.fmt
        nul = self.null
        name = self.var
        a = self.arg
        if vt == "Length":
            return "${#" + name + "}"
        else:
            stri = "${" + name

            # Depending on who generated the JSON, nul may be
            # a string or a boolean! In Python, non-empty strings
            # to True.
            if str(nul).lower() == "true":
                stri += ":"
            elif str(nul).lower() == "false":
                pass
            else:
                assert False

            stri += string_of_var_type(vt) + string_of_arg(a, quote_mode) + "}"

            return stri


# quote character
class QArgChar(ArgChar):
    NodeName = 'Q'
    arg: List[ArgChar]

    def __init__(self, arg: List[ArgChar]):
        self.arg = arg

    def __repr__(self):
        return f'Q({self.arg})'

    def format(self) -> str:
        chars = [arg_char.format() for arg_char in self.arg]
        joined_chars = "".join(chars)
        return '"{}"'.format(joined_chars)

    def json(self):
        json_output = make_kv(QArgChar.NodeName, self.arg)
        return json_output

    def pretty(self, quote_mode=UNQUOTED):
        param = self.arg
        return "\"" + string_of_arg(param, quote_mode=QUOTED) + "\""


#
class BArgChar(ArgChar):
    NodeName = 'B'
    node: Command

    def __init__(self, node: Command):
        self.node = node

    ## TODO: Implement
    # def __repr__(self):
    #     return f''

    def format(self) -> str:
        return '$({})'.format(self.node)

    def json(self):
        json_output = make_kv(BArgChar.NodeName, self.node)
        return json_output

    # def pretty(self, quote_mode=UNQUOTED):
    #     param = self.node
    #     return "$(" + param.pretty() + ")"

    def pretty(self, quote_mode=UNQUOTED):
        param = self.node
        return "$(" + param.pretty() + ")"
        # return "$(command)"


def string_of_arg(args, quote_mode=UNQUOTED):
    i = 0
    text = []
    while i < len(args):
        c = args[i].pretty(quote_mode=quote_mode)
        if c == "$" and (i + 1 < len(args)) and isinstance(args[i + 1], EArgChar):
            c = "\\$"
        text.append(c)

        i = i + 1

    text = "".join(text)

    return text


# E type char
def escaped(param):
    char = chr(param)
    return char
    # if char == "'":
    #     return "\\'"
    # elif char == "\\":
    #     return "\\\\"
    # elif char == "\n":
    #     return "\\n"
    # elif char == "\t":
    #     return "\\t"
    # elif char == "\r":
    #     return "\\r"
    # elif char == "\b":
    #     return "\\b"
    # elif (param >= ord(' ')) and (param <= ord('~')):
    #     return char
    # else:
    #     #        str1 =   "\\" \
    #     #               + chr (48 + int (param / 100)) \
    #     #               + chr (48 + ((int (param / 10)) % 10)) \
    #     #               + chr (48 + (param % 10));
    #     return "\\" + str(param)


# V type char
STRING_OF_VAR_TYPE_DICT = {
    "Normal": "",
    "Minus": "-",
    "Plus": "+",
    "Question": "?",
    "Assign": "=",
    "TrimR": "%",
    "TrimRMax": "%%",
    "TrimL": "#",
    "TrimLMax": "##",
    "Length": "#"
}


def string_of_var_type(var_type):
    if var_type in STRING_OF_VAR_TYPE_DICT:
        return STRING_OF_VAR_TYPE_DICT[var_type]
    exit(1)
