#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys
import json
import config
from flask import Blueprint
from flask import request, flash, render_template

from init import db
from models import UsrInfo
from methods import generate_token
from forms import UsrRegisterForm, UsrLoginForm

sys.path.append(config.METHODS_PATH)

users = Blueprint('user', __name__)


# 8.我的
# 用户注册
@users.route('/HelloSTU/usr_register/', methods=['GET', 'POST'])
def usr_register():
    form = UsrRegisterForm()
    if request.method == 'POST':
        name = form.name.data
        account = form.account.data
        password = form.password.data
        if name and account and password:
            try:
                new_usr = UsrInfo(name=name, account=account, password=password, permission='user')
                new_usr.hash_password(password)
                db.session.add(new_usr)
                db.session.commit()
                return '注册成功'
            except Exception as e:
                print(e)
                flash('注册失败')
                db.session.rollback()
                return '注册失败'
        else:
            return '参数出错'

    return render_template('upload.html', form=form)


# 用户登录
# {"id": 12, "name": "cxc", "account": "16xccheng3", "permission": "user",
#  "token": "MTU1MDQxNTY3MC4zMDQ3NTQzOmQzOGQ5MGQ1YmZhMmVjNWVlMjdiYjRiMzkyMjA3MjUzMTdkYTViMWE="}
@users.route('/HelloSTU/usr_login/', methods=['GET', 'POST'])
def usr_login():
    form = UsrLoginForm()
    if request.method == 'POST':
        account = form.account.data
        password = form.password.data
        temp = UsrInfo.query.filter_by(account=account).first()
        if not temp:
            return '未找到该用户'
        if temp.verify_password(password):
            dict = {}
            dict['id'] = temp.id
            dict['name'] = temp.name
            dict['account'] = temp.account
            dict['permission'] = temp.permission
            dict['token'] = generate_token(temp.id)
            return json.dumps(dict)
        else:
            return '密码错误'

    return render_template('upload.html', form=form)