import os
import re

from generate_feature_gen_command import generate_feature_gen_command_script

for file_name in os.listdir("../../../old/tests"):
    if file_name.startswith("test_"):
        with open(f"../../../old/tests/{file_name}", "r") as f:
            text = f.read()
            pattern = r"def test_.*_(\d+)\(\) -> None:"
            result = re.findall(pattern, text)
            case_num = max(list(map(int, result)))
            pattern = r'cmd_name = "(\w+)"'
            if re.search(pattern, text):
                cmd_name = re.search(pattern, text).group(1)
                if os.path.exists(f"../test_feature_gen_{cmd_name}.py"):
                    continue
                generate_feature_gen_command_script(cmd_name, case_num)
                with open(f"../test_feature_gen_{cmd_name}.py", "r") as f:
                    text2 = f.read()

                split_block1 = re.split("def", text)
                split_block2 = re.split("def", text2)
                new_block = [split_block2[0]]
                for i in range(1, len(split_block1)):
                    block1 = split_block1[i]
                    block2 = split_block2[i]
                    pattern = r"-> None:(.*?)cmd_inv"
                    if re.search(pattern, block1, re.DOTALL) and re.search(pattern, block2, re.DOTALL):
                        # Formatting
                        original_arg = re.search(pattern, block1, re.DOTALL).group(1)
                        original_arg = original_arg.replace(': List[FlagOption]', '').replace(": List[Operand]", "")
                        rows = []
                        for row in original_arg.split("\n"):
                            rows.append(f"    {row}")
                        original_arg = '\n'.join(rows)

                        replace_arg = re.search(pattern, block2, re.DOTALL).group(1)
                        block2 = block2.replace(replace_arg, original_arg)
                    else:
                        raise Exception("error")

                    pattern1 = r"== (\d+)"
                    expected_value_list = re.findall(pattern1, block1)
                    if len(expected_value_list) == 4:
                        config_input_value = int(expected_value_list[0])
                        config_output_value = int(expected_value_list[1])
                        file_value = int(expected_value_list[2]) + int(expected_value_list[3])

                        config_input_replace = 'self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_input()))'
                        config_output_replace = 'self.assertEqual(0, len(cmd_inv_with_feature.get_options_with_config_output()))'
                        file_replace = 'self.assertEqual(0, len(cmd_inv_with_feature.get_operands_with_file()))'

                        config_input_new = f'self.assertEqual({config_input_value}, len(cmd_inv_with_feature.get_options_with_config_input()))'
                        config_output_new = f'self.assertEqual({config_output_value}, len(cmd_inv_with_feature.get_options_with_config_output()))'
                        file_new = f'self.assertEqual({file_value}, len(cmd_inv_with_feature.get_operands_with_file()))'

                        block2 = block2.replace(config_input_replace, config_input_new)
                        block2 = block2.replace(config_output_replace, config_output_new)
                        block2 = block2.replace(file_replace, file_new)

                    new_block.append(block2)

                with open(f"../test_feature_gen_{cmd_name}.py", "w") as f:
                    f.write("def".join(new_block))

            else:
                print("不存在cmd_name")
                continue
