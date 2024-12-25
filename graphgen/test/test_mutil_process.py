import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List

import dockerfile
from dockerfile import Command


def processer(content):
    parsed_dockerfile = dockerfile.parse_string(content)
    # print(content)


dir_path = "/home/haoside/Desktop/input2"
output_path = "/home/haoside/Desktop/output2"
build_ctx = "/home/haoside/Desktop/aaa"
arg_list = []
files_name = os.listdir(dir_path)[:8]
print(files_name)
for file_name in files_name:
    file_path = os.path.join(dir_path, file_name)
    if os.path.isfile(file_path):
        new_output_path = os.path.join(output_path, os.path.splitext(file_name)[0] + "_script.cypher")
        content = open(file_path, "r").read()
        arg_list.append((content))

with ProcessPoolExecutor(max_workers=1) as executor:
    futures = {executor.submit(processer, arg): arg for arg in arg_list}
    for future in as_completed(futures, timeout=5):
        try:
            result = future.result()
            # Process the result
            print(result)
        except TimeoutError:
            print("Task timed out")
        except Exception as e:
            print(f"Task generated an exception: {e}")

print("success!")
