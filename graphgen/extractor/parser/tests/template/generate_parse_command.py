import os.path

from jinja2 import Environment, FileSystemLoader

# 配置模板环境
env = Environment(loader=FileSystemLoader('.'))

# 获取模板
template = env.get_template('./parse_command_template.txt')

# 命令
command = "node"
# 示例个数
case_num = 4

# 渲染模板
rendered_template = template.render(command=command.lower(), case_num=case_num)

# 输出渲染后的模板
# print(rendered_template)

# 强制写入
force = True
if not force and os.path.exists(f'../test_parse_{command}.py'):
    print("写入失败,文件已存在!")
else:
    if force:
        print("注意:已强制覆盖!")
    with open(f'../test_parse_{command}.py', 'w', encoding='utf-8') as f:
        f.write(rendered_template)
print("生成脚本成功!!!")
