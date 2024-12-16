import os
import re

data=dict()
file_names = []
cost_times = []
char_lengths = []
instruction_lengths = []


def calc_file_char_num(content):
    dockerfile_content = []
    for line in content.split('\n')[1:-1]:
        if line.strip():
            dockerfile_content.append(line)

    char_num = len("\n".join(dockerfile_content))
    return char_num


for file_name in os.listdir("./ENRIE-4-8k_result"):
    if file_name.endswith("-cost-time"):
        filename=file_name.split("###")[0]
        with open("./ENRIE-4-8k_result/" + file_name.replace("-cost-time", ""), "r", encoding="utf-8") as file:
            content = file.read()
            char_num = calc_file_char_num(content)

        with open("./ENRIE-4-8k_result/" + file_name, "r", encoding="utf-8") as file:
            lines= file.readlines()
            assert len(lines) == 2
            instruction_length = float(lines[0].strip())
            cost_time = float(lines[1].strip())

        file_names.append(filename)
        cost_times.append(cost_time)
        char_lengths.append(char_num)
        instruction_lengths.append(instruction_length)


