
cmd = "swift"
cmd_list = set()
with open("RUN_total.txt", "r") as file:
    for line in file:
        t = line.split(maxsplit=1)
        if t:
            cmd1 = t[0].strip()
            if cmd == cmd1:
                cmd_list.add(line)

with open(f"./example/{cmd}.txt", "w") as file:
    file.write(''.join(cmd_list))


