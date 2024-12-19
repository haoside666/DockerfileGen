import os.path

from jinja2 import Environment, FileSystemLoader

current_dir = os.path.dirname(__file__)


def generate_feature_gen_command_script(command: str):
    # 配置模板环境
    env = Environment(loader=FileSystemLoader(current_dir))

    # 获取模板
    template = env.get_template('transform_template.txt')

    # 渲染模板
    command = command.capitalize()
    rendered_template = template.render(command=command)

    # 输出渲染后的模板
    # print(rendered_template)

    # 强制写入
    force = False
    file_path = os.path.join(current_dir, f'../transformer/Transform{command}.py')
    if not force and os.path.exists(file_path):
        print("写入失败,文件已存在!")
    else:
        if force:
            print("注意:已强制覆盖!")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(rendered_template)
        print(f"生成Transform{command}.py脚本成功!!!")


if __name__ == '__main__':
    VALID_DIRECTIVES = [
        'FROM',
        'RUN',
        'CMD',
        'LABEL',
        'MAINTAINER',
        'EXPOSE',
        'ENV',
        'ADD',
        'COPY',
        'ENTRYPOINT',
        'VOLUME',
        'USER',
        'WORKDIR',
        'ARG',
        'ONBUILD',
        'STOPSIGNAL',
        'HEALTHCHECK',
        'SHELL'
    ]
    IGNORE_DIRECTIVES = [
        'LABEL',
        'MAINTAINER',
        'ONBUILD',
        'STOPSIGNAL',
        'HEALTHCHECK',
    ]
    map_dict = {}
    for command in VALID_DIRECTIVES:
        if command not in IGNORE_DIRECTIVES:
            # generate_feature_gen_command_script(command)
            map_dict[command] = f'Transform{command.capitalize()}'
    print(map_dict)
