# -*- coding:utf-8 -*-
# mysql配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Hello+stu2018@localhost/HelloSTU'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# json编码
JSON_AS_ASCII = False

# app密钥
SECRET_KEY = 'HelloSTU'

# 图片上传路径
UPLOADED_IMAGES_DEST = 'static/image'

# 自定义方法路径
METHODS_PATH = r'/home/cheng/python_workhouse'


# cache配置
CACHE = {
    "CACHE_TYPE": "redis",  # 类型
    "CACHE_REDIS_HOST": "127.0.0.1",  # 主机
    "CACHE_REDIS_PORT": 6379,  # 端口
    "CACHE_REDIS_PASSWORD": "ljgljgljg",  # 密码
    "CACHE_REDIS_DB": 15  # 数据库
}

# app启动设置
DEBUG = True
PORT = 8000
HOST = "0.0.0.0"