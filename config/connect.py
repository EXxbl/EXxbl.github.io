import os
from os import access

import redis
import pymysql
import time
import json
import datetime


class Insert_sql(object):
    def __init__(self, redis_db='feishu', mysql_db='feishu'):
        self.redis_config = {
            'host': '127.0.0.1',
            'port': 6379,
        }
        self.redis_password = ''
        self.redis_db = redis_db
        self.mysql_host = '127.0.0.1'
        self.mysql_port = 3306
        self.mysql_user = 'root'
        self.mysql_password = '123456'
        self.mysql_db = mysql_db

    def execute_sql(self, sqls):
        # 创建数据库连接
        db = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user,
                             password=self.mysql_password, db=self.mysql_db)
        # 创建数据库游标
        cursor = db.cursor()
        # 执行sql语句
        for sql in sqls:
            cursor.execute(sql)
        # 提交sql执行结果
        db.commit()
        # 关闭游标
        cursor.close()
        # 关闭链接
        db.close()
        return db

    # 创建表
    def create_mysql_table(self, table_name):
        # 创建数据库连接
        db = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user,
                             password=self.mysql_password, db=self.mysql_db)
        # 创建数据库游标
        cursor = db.cursor()
        # 查看表是否存在
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()
        # 如果表不存在，就创建表
        if not result:
            cursor.execute(f"CREATE TABLE {table_name} (file_name VARCHAR(255) PRIMARY KEY,rubbish_file VARCHAR(255))")
        # 提交sql执行结果
        db.commit()
        # 关闭游标
        cursor.close()
        # 关闭链接
        db.close()

    # 保存redis
    def redis_save(self, r_name, data, ex_time=None):
        redis_pool = redis.ConnectionPool(**self.redis_config, db=0)
        redis_client = redis.Redis(connection_pool=redis_pool)

        if ex_time:
            redis_client.set(f'{self.redis_db}:' + r_name, json.dumps(data, ensure_ascii=False), ex=ex_time)
        else:
            redis_client.rpush(f'{self.redis_db}:' + r_name, json.dumps(data, ensure_ascii=False))

        redis_client.close()

    # 获取redis
    def redis_lrange(self, r_name):
        redis_client = redis.Redis(**self.redis_config, db=0)
        data = redis_client.lrange(f'{self.redis_db}:' + r_name, 0, -1)
        redis_client.close()
        # 将每个 bytes 元素解码为 utf-8 字符串，并转换回 dict（如果是 JSON）
        try:
            decoded_data = [json.loads(item.decode('utf-8')) for item in data]
        except json.JSONDecodeError:
            decoded_data = [item.decode('utf-8') for item in data]
        return decoded_data

    # 查看栈的长度
    def redis_llen(self, r_name):
        redis_client = redis.Redis(**self.redis_config, db=0)
        key = f'{self.redis_db}:' + r_name

        length = redis_client.llen(key)
        redis_client.close()

        return length

    # 获取hash表的key
    def redis_hkeys(self,r_name):
        redis_client = redis.Redis(**self.redis_config, db=0)
        keys = redis_client.hkeys(f'{self.redis_db}:' + r_name)
        new_keys = []
        for key in keys:
            new_keys.append(key.decode('utf-8'))
        redis_client.close()
        return new_keys


    # 获取hash表的长度
    def redis_hlen(self,r_name):
        redis_client = redis.Redis(**self.redis_config, db=0)
        len = redis_client.hlen(f'{self.redis_db}:' + r_name)
        if len == 0:
            return None
        redis_client.close()
        return len

    # 第一个元素出栈
    def redis_pop(self, r_name):
        redis_client = redis.Redis(**self.redis_config, db=0)

        redis_result = redis_client.lpop(f'{self.redis_db}:' + r_name)
        if redis_result is None:
            return None
        redis_result = redis_result.decode('utf-8')
        redis_client.close()
        return redis_result

    # 删除hash表的元素
    def redis_hdel(self,r_name,r_key):
        redis_client = redis.Redis(**self.redis_config, db=0)
        redis_result = redis_client.hdel(f'{self.redis_db}:' + r_name,r_key)
        if redis_result != 1:
            return None
        redis_client.close()
        return redis_result

    def redis_get(self,r_name):
        redis_pool = redis.ConnectionPool(**self.redis_config, db=0)
        redis_client = redis.Redis(connection_pool=redis_pool)
        return redis_client.get(f'{self.redis_db}:' + r_name)


    def redis_hset(self, r_name, data):
        redis_pool = redis.ConnectionPool(**self.redis_config, db=0)
        redis_client = redis.Redis(connection_pool=redis_pool)

        key = list(data.keys())[0]
        value = {'value': list(data.values())[0], 'time': time.time()}
        redis_client.hset(f'{self.redis_db}:' + r_name, key, json.dumps(value, ensure_ascii=False))

        redis_client.close()

    def redis_hget(self, r_name, data):
        redis_pool = redis.ConnectionPool(**self.redis_config, db=0)
        redis_client = redis.Redis(connection_pool=redis_pool)
        value = redis_client.hget(f'{self.redis_db}:' + r_name, data).decode('utf-8')
        redis_client.close()
        if not value:
            return None
        if '{' in value and '}' in value:
            access_token = json.loads(value)['value']
            if time.time() - json.loads(value)['time'] > 3600 * 2:
                access_token = None
        else:
            access_token = value
        return access_token

    def redis_expire(self, r_name, ex_time):
        redis_pool = redis.ConnectionPool(**self.redis_config, db=0)
        redis_client = redis.Redis(connection_pool=redis_pool)
        key = f'{self.redis_db}:' + r_name
        redis_client.expire(key, ex_time)  # 设置过期时间（秒）
        redis_client.close()

    def redis_hgetall(self,key):
        redis_pool = redis.ConnectionPool(**self.redis_config, db=0)
        redis_client = redis.Redis(connection_pool=redis_pool)
        keys = redis_client.hgetall(self.redis_db+':'+key)
        redis_client.close()
        # 将bytes转换为字符串
        new_keys = {key.decode('utf-8'): value.decode('utf-8') for key, value in keys.items()}
        return new_keys

    def redis_del_list(self,key):
        redis_pool = redis.ConnectionPool(**self.redis_config, db=0)
        redis_client = redis.Redis(connection_pool=redis_pool)
        redis_client.delete(self.redis_db+':'+key)
        redis_client.close()
