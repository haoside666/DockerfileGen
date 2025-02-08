# 解析cypher脚本,生成实体sql语句
import re

from graphgen.config.definitions import ROOT_DIR
from graphparse.mysql_gen.mysql_link import MysqlLink


# 权重信息表
#   基础镜像
#   单包
#   文件工具包
#   工具包
def parse_cypher_script(cypher_script: str) -> dict:
    weight_dict = dict()

    pattern = r"MERGE \(([a-z0-9]+):([a-zA-Z]+) (.*)\)"

    result = re.findall(pattern, cypher_script)
    for match in result:
        hash_value = match[0]
        label_name = match[1]
        if hash_value in weight_dict:
            weight_dict[hash_value]["weight_value"] += 1
        else:
            weight_dict[hash_value] = {
                "label_name": label_name,
                "weight_value": 1
            }

    return weight_dict


def gen_weight_info_db(total_weight_dict):
    db = MysqlLink()
    datas = [
        (hash_value, info_dict["label_name"], info_dict["weight_value"])
        for hash_value, info_dict in total_weight_dict.items()
    ]
    db.insert_all_data_to_entity_weight_info_table(datas)


def clear_weight_info_db():
    db = MysqlLink()
    db.clear_weight_info_table()
    print("清空权重数据库成功!")


if __name__ == '__main__':
    cypher_script_path = f"{ROOT_DIR}/graph/script/Dockerfile_test_tool_package.cypher"
    with open(cypher_script_path, "r") as file:
        content = file.read()
        sql_result = parse_cypher_script(content)
