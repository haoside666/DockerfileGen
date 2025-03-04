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


def parse_cypher_script2(cypher_script: str) -> tuple[dict, set]:
    weight_dict = dict()
    relation_set = set()
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
    pattern = r"MERGE \(([a-z0-9]+)\)-\[:([a-zA-Z]+)\]->\(([a-z0-9]+)\)"
    r_result = re.findall(pattern, cypher_script)
    for match in r_result:
        obj1 = match[0]
        r_name = match[1]
        obj2 = match[2]
        relation_set.add((obj1, r_name, obj2))

    return weight_dict, relation_set


def parse_cypher_script3(cypher_script: str) -> dict:
    entity_dict = dict()
    pattern = r"MERGE \(([a-z0-9]+):([a-zA-Z]+) (.*)\)"

    result = re.findall(pattern, cypher_script)
    for match in result:
        hash_value = match[0]
        entity_content = match[2]
        if hash_value not in entity_dict:
            entity_dict[hash_value] = entity_content

    return entity_dict


def gen_weight_info_db(total_weight_dict):
    db = MysqlLink()
    datas = [
        (hash_value, info_dict["label_name"], info_dict["weight_value"])
        for hash_value, info_dict in total_weight_dict.items()
    ]
    db.insert_all_data_to_entity_weight_info_table(datas)


def gen_weight_info_by_neo4j_script_db(total_weight_dict):
    db = MysqlLink()
    datas = [
        (hash_value, info_dict["label_name"], info_dict["weight_value"])
        for hash_value, info_dict in total_weight_dict.items()
    ]
    db.insert_all_data_to_entity_weight_info_by_neo4j_script_table(datas)


def gen_relation_info_by_neo4j_script_db(total_relation_set):
    db = MysqlLink()
    db.insert_all_data_to_relation_weight_info_by_neo4j_script_table(list(total_relation_set))


def gen_entity_info_by_neo4j_script_db(entity_info_dict):
    db = MysqlLink()
    datas = [
        (hash_value, entity_content)
        for hash_value, entity_content in entity_info_dict.items()
    ]
    db.insert_all_data_to_entity_info_by_neo4j_script_table(datas)


def clear_weight_info_db():
    db = MysqlLink()
    db.clear_weight_info_table()
    print("清空权重数据库成功!")


if __name__ == '__main__':
    cypher_script_path = f"{ROOT_DIR}/graph/script/Dockerfile_test_tool_package.cypher"
    with open(cypher_script_path, "r") as file:
        content = file.read()
        sql_result = parse_cypher_script(content)
