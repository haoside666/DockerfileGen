import os
import re

for file_name in os.listdir("./提问模板"):
    with open("./提问模板/" + file_name, "r", encoding="utf-8") as file:
        content = ""
        k = 0
        for line in file:
            if line.strip() and line.split()[0].isupper():
                content += f"{k} {line}"
                k += 1
            else:
                content += line

        content = content.strip()

    with open("./提问模板/" + file_name, "w", encoding="utf-8") as file:
        file.write(content)
