# special_situation_1
# If one line starts with - and the next line starts with --, merge the two lines.
import sys


def is_startswith_hyphen(string: str):
    return string[0] == '-' and len(string) > 1 and string[1] != "-" and string.find("--") == -1


def handle_special_situation_1(text):
    lines = text.strip().split('\n')
    merged_lines = []

    i = 0
    while i < len(lines):
        current_line = lines[i]

        if is_startswith_hyphen(current_line) and i + 1 < len(lines) and lines[i + 1].startswith('--'):
            merged_lines.append(current_line + ', ' + lines[i + 1])
            i += 2
        else:
            merged_lines.append(current_line)
            i += 1

    output_text = '\n'.join(merged_lines)
    print(output_text)


handle_special_situation_1(sys.stdin.read())
