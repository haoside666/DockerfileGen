import re


class StringProcessor:
    def __init__(self, input_string: str):
        self.input_string: str = input_string

    def process(self) -> str:
        processed_string = self.input_string
        cmd_name = processed_string.split()[0]

        if cmd_name == "tar":
            pattern = r'\btar\s+([AcdrtuxGnSkUWOmpsMBIajJzZhplRvwOf]+)\b'
            if re.search(pattern, processed_string):
                processed_string = re.sub(pattern, lambda x: "tar -" + x.group(1), processed_string)
            else:
                pattern = r"(\s-[a-zA-Z]+)-\s"
                if re.search(pattern, processed_string):
                    processed_string = re.sub(pattern, lambda x: x.group(1) + " - ", processed_string)
        elif cmd_name in {"curl", "wget"}:
            pattern = r"(\s-[a-zA-Z]+)-\s"
            if re.search(pattern, processed_string):
                processed_string = re.sub(pattern, lambda x: x.group(1) + " - ", processed_string)

        return processed_string
