#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import time
import hmac
import base64
import random

from init import images
from models import UsrInfo


# ################################################### 通用函数定义 ##################################################### #
# repr返回值类型转dict--可针对不同个数的返回值first/all
def to_dict(temp, title):  # title表示抬头
    t_dict = {}
    for i in range(len(temp)):
        t_dict[title[i]] = eval(str(temp[i]))

    return t_dict


# 获取当前时间--返回（字符串）：2019-02-04 11:47:35
def local_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 生成随机16位的字符串--用于生成图片随机文件名
def random_str(length=16):
    base_str = 'qwertyuioplkjhgfdsazcxvbnm0123456789'

    return ''.join(random.choice(base_str) for i in range(length))


# 添加writer_name--用于用户post操作
def add_element1(temp, title):
    t_dict = {}
    for i in range(len(temp)):
        a = eval(str(temp[i]))
        a['writer_name'] = UsrInfo.query.filter_by(id=temp[i].writer_id).first().name
        t_dict[title[i]] = a

    return t_dict


# 添加writer_name和replied_name--用于用户post操作中的评论操作
def add_element2(temp, title):
    t_dict = {}
    for i in range(len(temp)):
        a = eval(str(temp[i]))
        a['writer_name'] = UsrInfo.query.filter_by(id=temp[i].writer_id).first().name
        if temp[i].replied_id != -1:
            a['replied_name'] = UsrInfo.query.filter_by(id=temp[i].replied_id).first().name
        else:
            a['replied_name'] = 'null'
        t_dict[title[i]] = a

    return t_dict


# 图片上传和转换
def upload_image(image):
    if image:
        # 获取文件的后缀
        suffix = os.path.splitext(image.filename)[1]
        # 生成随机的文件名
        filename = random_str() + suffix
        # 保存文件
        images.save(image, name=filename)
        # 获取文件的地址
        img_url = images.url(filename)
    else:
        img_url = None

    return img_url


# 生成token 密钥：用户id--用于用户登录
def generate_token(key, expire=3600):
    t_str = str(time.time() + expire)  # expire为有效时间,1个单位代表1秒
    t_byte = t_str.encode("utf-8")
    t_hash = hmac.new(str(key).encode("utf-8"), t_byte, 'sha1').hexdigest()  # sha1为安全哈希算法
    token = t_str+':'+t_hash
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


# 验证token 密钥：用户id--用于用户post操作中的验证
def certify_token(key, token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    if float(token_list[0]) < time.time():
        return False
    sha1 = hmac.new(str(key).encode("utf-8"), token_list[0].encode('utf-8'), 'sha1')
    if sha1.hexdigest() != token_list[1]:
        return False
    return True