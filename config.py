# #####################################################################################################################
# 名称：HelloSTU后端配置文件
# 作者：程晓聪
# 版本：1.0
# 修改：2019.2.2
# #####################################################################################################################


# -*- coding:utf-8 -*-
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Hello+stu2018@localhost/HelloSTU'
SQLALCHEMY_TRACK_MODIFICATIONS = False


JSON_AS_ASCII = False


SECRET_KEY = 'HelloSTU'


UPLOADED_IMAGES_DEST = 'static/image'


METHODS_PATH = r'/home/cheng/python_workhouse'


# cache配置
CACHE = {
    "CACHE_TYPE": "redis",  # 类型
    "CACHE_REDIS_HOST": "127.0.0.1",  # 主机
    "CACHE_REDIS_PORT": 6379,  # 端口
    "CACHE_REDIS_PASSWORD": "ljgljgljg",  # 密码
    "CACHE_REDIS_DB": 15  # 数据库
}


DEBUG = True
PORT = 8000
HOST = "0.0.0.0"