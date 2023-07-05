# FastAPI and SQLAlchemy

## 01 初始化

命令：`fas database --help`，从已有数据库或者表生成模型文件：

```bash
fas database --help

fas database create doc_extract --password="passwd" --host="192.168.1.242" --table_prefix=ext --save_path=../temp/test.py --tables="ext_big_file,ext_big_file_part"
```
