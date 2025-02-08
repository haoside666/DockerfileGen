import MySQLdb
import traceback

from graphgen.config.db_config import DATABASES

import sys

import pymysql


class MysqlLink(object):
    cur = None
    con = None

    def __init__(self, key="default"):
        try:
            host: str = DATABASES[key]['HOST']
            user: str = DATABASES[key]['USER']
            password: str = DATABASES[key]['PASSWORD']
            database: str = DATABASES[key]['NAME']
            port: int = int(DATABASES[key]['PORT'])
            if host == "":
                print("mysql_server_ip cannot be empty!!", file=sys.stderr)
                exit(1)
            self.con = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                charset='utf8',
            )
            self.cur = self.con.cursor()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("connect fail,error type:" + type(e).__name__)
            if "No route to host" in e.args[1]:
                print("The ip address or the mysql server is incorrect!!")
            elif "Access denied for user" in e.args[1]:
                print("The username or password is incorrect!!")
                print("Please check if your mysql configuration is correct!!")
            else:
                print(e.args[1])
            exit(2)
        except pymysql.Error as e:
            print("throw an exception，type:" + type(e).__name__)
            exit(3)

    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.con is not None:
            self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def clear_weight_info_table(self):
        try:
            sql = f'truncate table entity_weight_info'
            self.cur.execute(sql)
            self.con.commit()
        except Exception as e:
            print(traceback.format_exc())
            print(e.args[0])
            raise

    def insert_all_data_to_entity_weight_info_table(self, datas):
        try:
            sql = f'insert into entity_weight_info values(%s,%s,%s)'
            self.cur.executemany(sql, datas)
            self.con.commit()
        except Exception as e:
            print(traceback.format_exc())
            print(e.args[0])
            raise

    def get_max_weight_by_hash_values(self, hash_values):
        try:
            hash_values = tuple(hash_values)
            sql = f'select hash_value,weight_value from entity_weight_info where hash_value in {hash_values} ORDER BY weight_value desc LIMIT 1;'
            self.cur.execute(sql)
            result = self.cur.fetchone()
            return result[0]
        except Exception as e:
            print(traceback.format_exc())
            print(e.args[0])
            raise

    def get_all_hash_value_and_weight_value(self):
        try:
            sql = f'select hash_value,weight_value from entity_weight_info;'
            self.cur.execute(sql)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(traceback.format_exc())
            print(e.args[0])
            raise


if __name__ == '__main__':
    mysql_link = MysqlLink()
    mysql_link.insert_all_data_to_entity_weight_info_table([
        ("aaaa", "Image", 1),
        ("bbbb", "ExeCmd", 2),
    ])
