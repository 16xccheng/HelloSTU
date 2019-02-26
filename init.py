#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import config
from flask import Flask
from flask_script import Manager  # 文件拓展
from flask_bootstrap import Bootstrap  # 文件拓展
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_cache import Cache

# app定义
app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)


# 配置缓存
cache = Cache(app, config=config.CACHE)

# 设置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
# 创建数据库对象
db = SQLAlchemy(app)

# 设置json中文
app.config['JSON_AS_ASCII'] = config.JSON_AS_ASCII

# 配置上传文件（图片）的保存路径，[]中的内容要写成'UPLOADED_名字_DEST'，名字:创建上传对象时第一个参数大写
app.config['UPLOADED_IMAGES_DEST'] = os.path.join(os.getcwd(), config.UPLOADED_IMAGES_DEST)
# 设置文件（图片）大小限制(8M)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 8
# 创建文件（图片）上传对象(对象名,对象类型)
images = UploadSet('images', IMAGES)
# 配置对象(创建的app名,文件（图片）上传的对象)
configure_uploads(app, images)

# 设置密钥
app.secret_key = config.SECRET_KEY

# 蓝图
from API_communicate import communicate
app.register_blueprint(communicate, url_prefix='')
from API_content import content
app.register_blueprint(content, url_prefix='')
from API_goods import goods
app.register_blueprint(goods, url_prefix='')
from API_organization import organization
app.register_blueprint(organization, url_prefix='')
from API_user import user
app.register_blueprint(user, url_prefix='')