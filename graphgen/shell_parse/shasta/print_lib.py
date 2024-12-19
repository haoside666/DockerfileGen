UNQUOTED = 0  # everything escaped
QUOTED = 1  # only escape special characters
HEREDOC = 2  # like QUOTED, but _don't_ escape double quotes
QUOTE_MODES = [UNQUOTED, QUOTED, HEREDOC]


def braces(s):
    return "{ " + s + " ; }"


def intercalate(p, ss):
    str = p.join(ss)
    return str


def parens(s):
    return f"( {s} )"


## TODO: Fix this
def separated(f, l):
    return " ".join(map(f, l))


def show_unless(expected, actual):
    if expected == actual:
        return ""
    else:
        return str(actual)


def background(s):
    return "{ " + s + " & }"


def fresh_marker(heredoc):
    respectsFound = set();

    for line in heredoc.split('\n'):
        respects = 0;

        if ((len(line) > 2) and (line[0] == 'E') and (line[1] == 'O')):
            for i in range(2, len(line)):
                if (line[i] == 'F'):
                    respects = i - 2;

            respectsFound.add(respects);

    i = 0;
    while (True):
        if (not (i in respectsFound)):
            return "EOF" + ("F" * i);

        i = i + 1;


# This version may give an unnecessarily long EOFFFF... (and therefore won't
# match the OCaml output but it is still correct w.r.t. giving a fresh
# marker, and uses less memory than fresh_marker above).
def fresh_marker0(heredoc):
    maxRespects = 0

    for line in heredoc.split('\n'):
        respects = 0

        if (len(line) > 2) and (line[0] == 'E') and (line[1] == 'O'):
            for i in range(2, len(line)):
                if line[i] == 'F':
                    respects = i - 1

            maxRespects = max(maxRespects, respects)

    return "EOF" + ("F" * maxRespects)
