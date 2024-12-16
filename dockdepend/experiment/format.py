import os
import re

for filename in os.listdir("./文心一言_result"):
    s = ""
    with open(f"./文心一言_result/{filename}", "r", encoding="utf-8") as file:
        r_list = []
        for line in file:
            if line.startswith("[(") or line.startswith(" ("):
                t = line.split("(")[1].split(")")[0].split(", ")

                if len(t) == 2:
                    num1 = t[0]
                    num2 = t[1]
                    r_list.append(line)
                    text = re.sub(r'\d+', '', line)
                    text = text.replace("(", "(" + num2).replace(")", num1 + ")")
                    s += text
                else:
                    s += line
            else:
                s += line
    with open(f"./文心一言_result_new/{filename}", "w", encoding="utf-8") as file:
        file.write(s)
