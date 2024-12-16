from typing import List


def make_kv(key, val) -> List:
    return [key, val]


def print_to_file(file_path, content):
    with open(file_path, "a") as file:
        file.write(content)
