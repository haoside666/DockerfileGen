import re
import sys
import json


# For the all commands,Combination of the following three cases
# len=1 -f or --flag
# len=2 -f --flag or -o ARG or --opt ARG
# len=3 -o --opt ARG or -f1  -f2 --flag or -f --flag1 --flag2
# len=4 -o ARG --opt ARG or -f --flag1 --flag2 --flag3
# len=4+ -f describe...

def find_match(line, past_flags):
    # store all flags & options in line
    xbd_args = []

    line = re.sub(r"\[|\]", '', line)
    line = re.sub(r"<|>", '', line)
    line = line.replace("=", " ")
    phrases = re.split(r"[, ]+", line)

    phrase_parts = [i.strip() for i in phrases if i != '']

    if len(phrase_parts) == 0:
        pass
    elif len(phrase_parts) == 1:
        if re.match(r"^-[-]*[a-z0-9-.#]*$", phrase_parts[0]) or re.match(r"^-[-]*[A-Z]$", phrase_parts[0]):
            flag = re.sub("-", '', phrase_parts[0])
            if flag not in past_flags:
                xbd_args.append(phrase_parts[0])
    elif len(phrase_parts) == 2:
        if is_startswith_hyphen(phrase_parts[0]) and phrase_parts[1].startswith("--"):
            flag = re.sub("-", '', phrase_parts[0])
            if flag not in past_flags:
                past_flags.add(flag)
                for item in phrase_parts:
                    xbd_args.append(item)
        elif phrase_parts[0].startswith("-") and not phrase_parts[1].startswith("-"):
            flag = re.sub("-", '', phrase_parts[0])
            if flag not in past_flags:
                past_flags.add(flag)
                xbd_args.append(phrase_parts)
    elif len(phrase_parts) == 3:
        if is_startswith_hyphen(phrase_parts[0]) and phrase_parts[1].startswith("-"):
            flag = re.sub("-", '', phrase_parts[0])
            if flag not in past_flags:
                past_flags.add(flag)
                if not phrase_parts[2].startswith("-"):
                    xbd_args.append(phrase_parts)
                else:
                    for item in phrase_parts:
                        xbd_args.append(item)
    elif len(phrase_parts) == 4:
        if is_startswith_hyphen(phrase_parts[0]) and phrase_parts[2].startswith("--"):
            flag = re.sub("-", '', phrase_parts[0])
            if flag not in past_flags:
                past_flags.add(flag)
                if phrase_parts[1] == phrase_parts[3]:
                    xbd_args.append(phrase_parts[:1] + phrase_parts[2:])
                elif phrase_parts[1].startswith("--") and phrase_parts[3].startswith("--"):
                    for item in phrase_parts:
                        xbd_args.append(item)
    else:
        if re.match(r"^-[-]*[a-z0-9-.#]*$", phrase_parts[0]) or re.match(r"^-[-]*[A-Z]$", phrase_parts[0]):
            flag = re.sub("-", '', phrase_parts[0])
            if flag not in past_flags:
                past_flags.add(flag)
                xbd_args.append(phrase_parts[0])
    # return xbd flags & options in line
    return (xbd_args, past_flags)


# For the system's own commands
def find_match1(line, past_flags):
    # TODO: for mv, it recognizes 2 options as flags: -S and -t (manually fixed for now)
    """
    Patterns to match (will be separated with ", "):
       ['--opt ARG', '--opt=ARG', '--opt[=ARG]', '-o ARG', '-O ARG'
        '-o=ARG', '-O=ARG', '-opt[=ARG]', '-f', '-F', '--flag']

    Patterns NOT to match: 
        ['-ARG', '--ARG', 'command descriptions']
    """
    # remove "[" and "]" from line
    line = re.sub(r"\[|\]", '', line)

    # store all flags & options in line
    xbd_args = []

    # arguments are comma-separated
    phrases = re.split(", ", line)

    # parse line and get xbd flags & options
    for i in range(len(phrases)):
        # remove starting and ending spaces
        phrases[i] = phrases[i].strip()

        # option flag and argument separated by space or equal sign
        if "=" in phrases[i]:
            phrase_parts = re.split(r"=", phrases[i])
        else:
            phrase_parts = re.split(r"\s+", phrases[i])

        if len(phrase_parts) >= 1 and (
                re.match(r"^-[-]*[a-z][a-z-]*$", phrase_parts[0]) or re.match(r"^-[-]*[A-Z]$", phrase_parts[0])):
            flag = re.sub("-", '', phrase_parts[0])
            # ignore duplicate flags
            if flag not in past_flags:
                past_flags.add(flag)
                if (len(phrase_parts) > 1) and (re.match(r"^[A-Z]+$", phrase_parts[1])):
                    xbd_args.append([phrase_parts[0], phrase_parts[1]])
                else:
                    xbd_args.append(phrase_parts[0])

    # return xbd flags & options in line
    return (xbd_args, past_flags)


# For additional downloaded commands,e.g. pip, curl, etc.
def find_match2(line, past_flags):
    """
    --styled-output
    -i, --include
    --keepalive-time <seconds>
    -e,--editable <path/url>
    -m, --max-time <seconds>
    Patterns to match (will be separated with ", "):
       ['--opt <ARG>', '-o,--opt <ARG>','-o, --opt <ARG>'
        '-f, --flag', '--flag']

    --user Install using the user scheme.
    Patterns NOT to match:
        ['-ARG', '--ARG', 'command descriptions']
    """
    # store all flags & options in line
    xbd_args = []

    phrases = re.split(r"[, ]+", line)

    phrase_parts = [i.strip() for i in phrases if i != '']

    if len(phrase_parts) >= 1 and (
            re.match(r"^-[-]*[a-z0-9-.#]*$", phrase_parts[0]) or re.match(r"^-[-]*[A-Z]$", phrase_parts[0])):
        flag = re.sub("-", '', phrase_parts[0])
        if flag not in past_flags:
            past_flags.add(flag)
            last_element: str = phrase_parts[-1]
            if last_element[0] == "<" and last_element[-1] == ">":
                phrase_parts[-1] = last_element[1:-1].upper()
                xbd_args.append(phrase_parts)
            elif last_element[0] == "-":
                for item in phrase_parts:
                    xbd_args.append(item)

    # return xbd flags & options in line
    return (xbd_args, past_flags)


# For special situation1 command,e.g. wget, etc.
def find_match3(line, past_flags):
    """
    -R rejlist, --reject rejlist
    -D domain-list, --domains=domain-list
    --exclude-domains domain-list
    --ignore-tags=list
    -H, --span-hosts
    -e option, see the GNU Info entry for wget.
    Patterns to match (will be separated with ", "):
       ['--opt ARG', '--opt=ARG', '-o ARG,--opt ARG','-o ARG, --opt=ARG'
        '-f', '--flag', '-f, --flag']

    --user Install using the user scheme.
    Patterns NOT to match:
        ['-ARG', '--ARG', 'command descriptions']
    """
    # store all flags & options in line
    xbd_args = []

    line = line.replace("=", " ")
    phrases = re.split(r"[, ]+", line)

    phrase_parts = [i.strip() for i in phrases if i != '']

    if len(phrase_parts) == 1:
        if re.match(r"^-[-]*[a-z0-9-.#]*$", phrase_parts[0]) or re.match(r"^-[-]*[A-Z]$", phrase_parts[0]):
            flag = re.sub("-", '', phrase_parts[0])
            if flag not in past_flags:
                xbd_args.append(phrase_parts[0])
    elif len(phrase_parts) == 2:
        if is_startswith_hyphen(phrase_parts[0]) and phrase_parts[1].startswith("--"):
            flag = re.sub("-", '', phrase_parts[0])
            if flag not in past_flags:
                past_flags.add(flag)
                for item in phrase_parts:
                    xbd_args.append(item)
        elif phrase_parts[0].startswith("--") and not phrase_parts[1].startswith("-"):
            flag = re.sub("-", '', phrase_parts[0])
            if flag not in past_flags:
                past_flags.add(flag)
                xbd_args.append(phrase_parts)
    elif len(phrase_parts) == 4:
        if re.match(r"^-[-]*[a-z0-9-.#]*$", phrase_parts[0]) or re.match(r"^-[-]*[A-Z]$", phrase_parts[0]):
            flag = re.sub("-", '', phrase_parts[0])
            if flag not in past_flags:
                past_flags.add(flag)
                if phrase_parts[1] == phrase_parts[3] and phrase_parts[2].startswith("--"):
                    xbd_args.append(phrase_parts[:1] + phrase_parts[2:])
    # return xbd flags & options in line
    return (xbd_args, past_flags)


def is_startswith_hyphen(string: str):
    return string[0] == '-' and len(string) > 1 and string[1] != "-"


def parse_args(args):
    """
    Flags: ['--flag']; ['-F']; ['-F', '--flag']
    Options: [['-o', 'ARG']]; [['--opt', 'ARG']]; [['-o', 'ARG'], ['--opt', 'ARG']]
    """
    args_dict = {"flag": [], "option": []}
    for line_args in args:
        if all([type(arg) == str for arg in line_args]):
            args_dict["flag"].append(list(line_args))
        else:
            for arg in line_args:
                if type(arg) == str:
                    args_dict["flag"].append(arg)
                else:
                    args_dict["option"].append(arg)
    return args_dict


def parse_lines(lines):
    """
    Return list of args in man page as JSON object.
    """
    # keep track of past flags & ignore duplicates 
    past_flags = set()

    # list of xbd args
    args = []
    for line in lines:
        line_args, past_flags = match_fun(line, past_flags)
        if line_args != []:
            args.append(line_args)

    # parse and return args
    return parse_args(args)


def parse(lines):
    args_dict = parse_lines(lines)
    json_formatted_args = json.dumps(args_dict, indent=4)
    print(json_formatted_args)


# # For the system's own commands: grep
# s1 = '''
# -P, --perl-regexp
# -e PATTERNS, --regexp=PATTERNS
# -f FILE, --file=FILE
# -i, --ignore-case
# --no-ignore-case
# '''
#
# # For additional downloaded commands: curl
# s2 = '''
# --create-dirs
# --crlf (FTP SMTP) Convert LF to CRLF in upload. Useful for MVS (OS/390).
# --crlfile <file>
# --data-ascii <data>
# -d, --data <data>
# --delegation <LEVEL>
# --digest
# -q, --disable
# '''
# # For special situation1 command: wget
# s3 = '''
# -c --conf file
# --debug
# --extrausers
# --firstgid id
# --force-badname
# -g --gid ID
# -h  --help
# --lastgid id
# -q  --quiet
# --system
# --verbose
# -v --version
# '''
# match_fun = find_match
# lines = s3.split("\n")
# parse(lines)

# # For common command
# s = '''
# -9
# --add
# -6  --ipv6
# -C path
# --abbrev length
# -b --branch branch
# -3  --3way  --no-3way
# -v  -vv  --verbose
# -f config-file --file config-file
# -a  --all  --append  --text
# '''
# match_fun = find_match
# lines = s.split("\n")
# parse(lines)


if len(sys.argv) != 2:
    print("Usage: python3 args-to-json.py find_matches_type")
    exit(1)
find_match_type = sys.argv[1]
if find_match_type == "0":
    match_fun = find_match
elif find_match_type == "1":
    match_fun = find_match1
elif find_match_type == "2":
    match_fun = find_match2
elif find_match_type == "3":
    match_fun = find_match3
parse(sys.stdin)
