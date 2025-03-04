import logging
import unittest
from concurrent.futures import ProcessPoolExecutor

from graphgen.config.definitions import ROOT_DIR
from graphgen.graph.Entity.EntityNode import *
from graphparse.mysql_gen.mysql_gen import parse_cypher_script, gen_weight_info_db, clear_weight_info_db, gen_weight_info_by_neo4j_script_db, parse_cypher_script2, \
    gen_relation_info_by_neo4j_script_db, gen_entity_info_by_neo4j_script_db, parse_cypher_script3
from graphparse.mysql_gen.mysql_link import MysqlLink
from graphparse.neo4j_reader.neo4j_reader import Neo4jConnection

LOG_PATH = os.path.abspath(f"{ROOT_DIR}/../logs/script_build.log")


# 创建日志
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler(filename=LOG_PATH, mode="a", encoding='utf-8')
# formatter = logging.Formatter('[{levelname}:{asctime}:{module}:{funcName}:{lineno}] {message}', style='{')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

def clear_file(file_path):
    with open(file_path, 'w') as file:
        file.truncate(0)


class TestBatchScriptToBuildGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.script_dir_path = "/home/haoside/Desktop/output"

    def test_single_script(self):
        filename = "bartixxx32___hidden-eye###174526###4d82cb4515b4d36cb9080f7c76df076ca0580910_script.cypher"
        script_path = f"/home/haoside/Desktop/output/{filename}"
        conn = Neo4jConnection()
        with open(script_path, "r") as file:
            cypher_script = file.read()
        conn.run_script(cypher_script)
        conn.close()

    def test_re_run_single_script(self):
        conn = Neo4jConnection()
        with open(f"{ROOT_DIR}/../logs/error_build.log", "r") as file:
            for line in file.readlines():
                try:
                    filename = line.replace("脚本构建错误！", "").strip()
                    script_path = f"/home/haoside/Desktop/output/{filename}"
                    with open(script_path, "r") as file:
                        cypher_script = file.read()
                        conn.run_script(cypher_script)
                except Exception as e:
                    with open(f"{ROOT_DIR}/../logs/error_build2.log", "a") as f:
                        f.write(f"{filename}脚本重新运行错误！\n")
        conn.close()

    @staticmethod
    def process_cypher_script(script_dir_path, file_name):
        with Neo4jConnection() as conn:
            script_path = os.path.join(script_dir_path, file_name)
            with open(script_path, "r") as file:
                cypher_script = file.read()
            try:
                if cypher_script:
                    conn.run_script(cypher_script)
                with open(LOG_PATH, "a") as file:
                    file.write(f"成功处理脚本: {file_name}\n")
                return file_name
            except Exception as e:
                with open(LOG_PATH, "a") as file:
                    file.write(f"处理文件 {file_name} 时出错: {e}\n")
                return None
            finally:
                pass
                # os.remove(script_path)

    @staticmethod
    def process_cypher_script_with_weight(script_dir_path, file_name):
        script_path = os.path.join(script_dir_path, file_name)
        with open(script_path, "r") as file:
            cypher_script = file.read()
        weight_dict = parse_cypher_script(cypher_script)
        return weight_dict

    @staticmethod
    def process_cypher_script_with_weight2(script_dir_path, file_name):
        script_path = os.path.join(script_dir_path, file_name)
        with open(script_path, "r") as file:
            cypher_script = file.read()
        weight_dict, relation_set = parse_cypher_script2(cypher_script)
        return weight_dict, relation_set

    @staticmethod
    def process_cypher_script_with_weight3(script_dir_path, file_name):
        script_path = os.path.join(script_dir_path, file_name)
        with open(script_path, "r") as file:
            cypher_script = file.read()
        entity_dict = parse_cypher_script3(cypher_script)
        return entity_dict

    def test_batch_script_to_build_graph(self):
        # 清空日志文件
        clear_file(LOG_PATH)
        # 清空neo4j数据库
        conn = Neo4jConnection()
        conn.clear()
        conn.close()
        # 清空权重数据库
        clear_weight_info_db()
        # 要求以.cypher结尾
        cypher_files = [file_name for file_name in os.listdir(self.script_dir_path) if file_name.endswith(".cypher")]

        # 创建neo4j数据库
        try:
            with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
                futures = [
                    executor.submit(self.process_cypher_script, self.script_dir_path, file_name)
                    for file_name in cypher_files
                ]
                # for future in as_completed(futures):
                #     try:
                #         result = future.result()
                #         # Process the result
                #         print(result)
                #     except TimeoutError:
                #         print("Task timed out")
                #     except Exception as e:
                #         print(f"Task generated an exception: {e}")
        except Exception as e:
            # print(total_handled_file)
            print(e.args)
            exit(1)

    def test_generate_weight_db(self):
        with open(LOG_PATH, "r") as file:
            content = file.read()
            file_names = re.findall("成功处理脚本: (.*)\n", content)

        total_handled_file = file_names
        # 创建权重数据库
        total_weight_dict = dict()
        for file_name in total_handled_file:
            weight_value = self.process_cypher_script_with_weight(self.script_dir_path, file_name)

            for hash_value, info_dict in weight_value.items():
                if hash_value in total_weight_dict:
                    total_weight_dict[hash_value]["weight_value"] += info_dict["weight_value"]
                else:
                    total_weight_dict[hash_value] = info_dict

        gen_weight_info_db(total_weight_dict)

    def test_add_weight_to_graph(self):
        with Neo4jConnection() as conn, MysqlLink() as db:
            weight_info = db.get_all_hash_value_and_weight_value()
            conn.add_weight_to_graph(weight_info)

    def test_reset_tool_pkg_weight_info(self):
        with Neo4jConnection() as conn:
            conn.reset_tool_pkg_weight_info()

    def test_generate_weight_by_neo4j_script_db(self):
        total_handled_file = os.listdir(self.script_dir_path)
        # 创建权重数据库
        total_weight_dict = dict()
        total_relation_set = set()
        for file_name in total_handled_file:
            weight_value, relation_set = self.process_cypher_script_with_weight2(self.script_dir_path, file_name)

            for hash_value, info_dict in weight_value.items():
                if hash_value in total_weight_dict:
                    total_weight_dict[hash_value]["weight_value"] += info_dict["weight_value"]
                else:
                    total_weight_dict[hash_value] = info_dict
            total_relation_set.update(relation_set)

        gen_weight_info_by_neo4j_script_db(total_weight_dict)
        gen_relation_info_by_neo4j_script_db(total_relation_set)

    def test_generate_entity_info_db(self):
        total_handled_file = os.listdir(self.script_dir_path)
        # 创建权重数据库
        total_entity_dict = dict()

        for file_name in total_handled_file:
            entity_dict = self.process_cypher_script_with_weight3(self.script_dir_path, file_name)
            total_entity_dict.update(entity_dict)

        gen_entity_info_by_neo4j_script_db(total_entity_dict)
