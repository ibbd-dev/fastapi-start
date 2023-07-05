# -*- coding: utf-8 -*-
#
# 数据库相关命令
# Author: caiyingyao
# Email: cyy0523xc@gmail.com
# Created Time: 2022-01-20
import re
import os


class Database:
    """数据库相关命令
    从已有的数据库表生成模型等

    Examples:
        [开发中]初始化及生成相关文件:
            fas database init
        从已有数据库中生成模型文件:
            fas database create
        示例：
            fas database create doc_extract --password="passwd" --host="192.168.1.242" --table_prefix=ext --save_path=../temp/test.py --tables="ext_big_file,ext_big_file_part"
    """

    def init(self):
        """数据库操作初始化及生成相关文件
        """
        # TODO
        print("开发中......")

    def create(self, db_name: str, save_path: str = '', user: str = 'root', password: str = '',
               host: str = '127.0.0.1', port: int = 3306, chartset: str = 'utf8',
               tables: str = '', table_prefix: str = ''):
        """从指定数据库中生成模型文件，并存储到一个python文件中

        Args:
            db_name (str): 数据库名
            save_path (str): 模型文件的保存路径
            user (str, optional): 数据库用户名. Defaults to 'root'.
            password (str, optional): 数据库密码. Defaults to ''.
            host (str, optional): 数据库连接host. Defaults to '127.0.0.1'.
            port (int, optional): 数据库连接端口号. Defaults to 3306.
            chartset (str, optional): 数据库连接编码. Defaults to 'utf8'.
            tables (str, optional): 需要生成模型的表名，多个表则用英文逗号进行分隔，不传或者为空则整库生成模型. Defaults to ''.
            table_prefix (str, optional): 表名前缀，如表名为pre_table1，其中pre为前缀，可以使用该参数统一去除模型名的前缀. Defaults to ''.
        """
        if '"' in password:
            raise Exception(f"password中包含了双引号")

        # 生成模型文件
        command = f"sqlacodegen mysql+pymysql://\"{user}\":\"{password}\"@{host}:{port}/{db_name}?charset={chartset}"
        if save_path:
            if os.path.isfile(save_path):
                raise Exception(f"目标文件已经存在：{save_path}")
            command += f" --outfile \"{save_path}\""
        if tables:
            command += f" --tables \"{','.join(tables)}\""
        resp = os.system(command)
        # print("-->", resp)
        # print(command)
        if save_path and not os.path.isfile(save_path):
            raise Exception(f"输出到目标文件{save_path}失败，请检查参数等是否正确")

        # 处理表名前缀
        table_prefix = table_prefix.strip()
        table_prefix = table_prefix.strip('_')
        if table_prefix and not save_path:
            raise Exception("table_prefix参数需要和save_path参数一起使用")
        if save_path and table_prefix:
            with open(save_path, encoding='utf8') as f:
                code = f.read()

            table_prefix = table_prefix.title()
            code = re.sub(f"\nclass {table_prefix}", "\nclass ", code)
            # 覆盖旧文件
            with open(save_path, 'w', encoding='utf8') as f:
                f.write(code)


if __name__ == "__main__":
    import fire
    # python database_cmd.py create doc_extract --password="passwd" --host="192.168.1.242" --table_prefix=ext --save_path=../temp/test.py --tables="ext_big_file,ext_big_file_part"
    fire.Fire(Database)
