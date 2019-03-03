#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import json
import config
import requests

from flask import Blueprint
from flask import request, flash, render_template

from init import db
from models import UsrInfo, WxUser
from methods import generate_token, generate_rdSession, certify_rdSession
from forms import UsrRegisterForm, UsrLoginForm, WxLoginForm, WxUpdateForm

sys.path.append(config.METHODS_PATH)

user = Blueprint('API_user', __name__)


# 8.我的
# 用户注册
@user.route('/register/', methods=['GET', 'POST'])
def Register():
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
@user.route('/login/', methods=['GET', 'POST'])
def Login():
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


# 小程序用户登录
@user.route('/wx/login/', methods=['POST'])
def Wxlogin():
    if request.method == 'POST':
        js_code = request.json['code']  # 坑，要清楚前端发送的类型
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code'.format(
            APPID=config.APPID, SECRET=config.APPSECRET, JSCODE=js_code)
        response = requests.get(url)
        print('这里这里这里'+response.text)
        if ('openid', 'session_key' in response.text)[-1]:
            try:
                dict = eval(response.text)
                new_usr = WxUser(openid=dict['openid'], session_key=dict['session_key'], gender=0)
                db.session.add(new_usr)
                db.session.commit()
                rdSession = generate_rdSession(dict['openid'], dict['session_key'])
                temp = WxUser.query.filter_by(session_key=dict['session_key']).first()
                message = {}
                message['id'] = temp.id
                message['rdSession'] = rdSession
                return json.dumps(message)
            except Exception as e:
                print(e)
                return '登录失败1'
        else:
            return '登录失败2'
    else:
        return '失败'


# 小程序用户信息更新
@user.route('/wx/update/', methods=['GET', 'POST'])
def Wxupdate():
    form = WxUpdateForm()
    if request.method == 'POST':
        id = form.id.data
        temp = WxUser.query.filter_by(id=id).first()
        rdSession = form.rdSession.data  #
        if certify_rdSession(temp.openid, temp.session_key, rdSession):
            name = form.name.data
            image = form.image.data
            city = form.city.data
            country = form.country.data
            gender = form.gender.data
            language = form.language.data
            province = form.province.data
            try:
                userinfo = WxUser.query.filter_by(id=id).first()
                userinfo.name = name
                userinfo.image = image
                userinfo.city = city
                userinfo.country = country
                userinfo.gender = gender
                userinfo.language = language
                userinfo.province = province
                db.session.commit()
                return '更新成功'
            except Exception as e:
                print(e)
                return '更新失败'
        else:
            return '登录超时'
    return render_template('upload.html', form=form)
