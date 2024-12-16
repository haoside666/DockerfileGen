import os.path

from jinja2 import Environment, FileSystemLoader

current_dir = os.path.dirname(__file__)


def generate_feature_gen_command_script(command: str, case_num: int):
    # 配置模板环境
    env = Environment(loader=FileSystemLoader(current_dir))

    # 获取模板
    template = env.get_template('command_feature_extract_template.txt')

    # 渲染模板
    rendered_template = template.render(command=command.lower(), case_num=case_num)

    # 输出渲染后的模板
    # print(rendered_template)

    # 强制写入
    force = False
    file_path = os.path.join(current_dir, f'../test_feature_gen_{command}.py')
    if not force and os.path.exists(file_path):
        print("写入失败,文件已存在!")
    else:
        if force:
            print("注意:已强制覆盖!")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(rendered_template)
        print(f"生成test_feature_gen_{command}.py脚本成功!!!")


if __name__ == '__main__':
    # 命令
    command = "tar"
    # 示例个数
    case_num = 7
    generate_feature_gen_command_script(command, case_num)
