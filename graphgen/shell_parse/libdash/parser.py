import os
from .ast import of_node
from ._dash import *
from graphgen.exception.CustomizedException import ParsingException

LIBDASH_LIBRARY_PATH = None


def libdash_library_path():
    global LIBDASH_LIBRARY_PATH

    if LIBDASH_LIBRARY_PATH is not None:
        return LIBDASH_LIBRARY_PATH

    FILE_PATH = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
    LIBDASH_LIBRARY_PATH = os.path.join(FILE_PATH, "libdash.so")
    return LIBDASH_LIBRARY_PATH


EOF_NLEFT = -99;  # libdash/src/input.c


# This is a mix of dash.ml:parse_next and parse_to_json.ml.
def parse(inputPath, init=True):
    """
    Parses the file at `inputPath` to an AST.

    `init` determines whether libdash should be initialized; set it to `False` after the first call.
    """
    lines = []

    libdash = CDLL(libdash_library_path())

    if (init):
        initialize(libdash)

    if (inputPath == "-"):
        setinputtostdin(libdash)
    else:
        setinputfile(libdash, inputPath)

        fp = open(inputPath, 'r')
        for line in fp:
            lines.append(line)
        fp.close()
    # struct parsefile *parsefile = &basepf;  /* current input file */
    # Get the value of parsefile (not &parsefile)!
    parsefile_ptr_ptr = addressof(parsefile.in_dll(libdash, "parsefile"))
    parsefile_ptr = cast(parsefile_ptr_ptr, POINTER(POINTER(parsefile)))
    parsefile_var = parsefile_ptr.contents

    smark = init_stack(libdash)

    NEOF = addressof(c_int.in_dll(libdash, "tokpushback"))
    NERR = addressof(c_int.in_dll(libdash, "lasttoken"))

    while (True):
        linno_before = parsefile_var.contents.linno - 1;  # libdash is 1-indexed

        n_ptr_C = parsecmd_safe(libdash, False)

        linno_after = parsefile_var.contents.linno - 1;  # libdash is 1-indexed
        nleft_after = parsefile_var.contents.nleft

        if (n_ptr_C == None):  # Dash.Null
            pass
        elif (n_ptr_C == NEOF):  # Dash.Done
            break
        elif (n_ptr_C == NERR):  # Dash.Error
            raise ParsingException()
        else:
            if (nleft_after == EOF_NLEFT):
                linno_after = linno_after + 1;  # The last line wasn't counted

                if (inputPath != "-"):
                    ## Both of these assertions check "our" assumption with respect to the final parser state
                    ## and are therefore not necessary if they become an issue.
                    assert ((linno_after == len(lines)) or (linno_after == len(lines) + 1))

                    # Last line did not have a newline
                    assert (len(lines[-1]) > 0 and (lines[-1][-1] != '\n'))
            else:
                assert (nleft_after == 0);  # Read whole lines

            n_ptr = cast(n_ptr_C, POINTER(union_node))

            new_ast = of_node(n_ptr)

            if (inputPath != "-"):
                parsedLines = "".join(lines[linno_before:linno_after])
            else:
                ## When parsing from stdin there is no way to save the lines
                parsedLines = None

            yield (new_ast, parsedLines, linno_before, linno_after)

            pop_stack(libdash, smark)
