#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys
import json
import config
from flask import Blueprint
from operator import attrgetter  # 排序操作
from flask import request, flash, render_template

from init import cache, db
from methods import to_dict, upload_image
from forms import SceneryForm, PlaceForm, PlayForm
from models import Scenery, PlaceC, Place, Message, PlayC, Play, QuestionC, Question, UseC, Use

sys.path.append(config.METHODS_PATH)

content = Blueprint('API_content', __name__)


# 1.景点
# 请求景点信息--输入：名称--返回：具体信息
# '{'id':6,'name':'2019.2.16','content':'2019.2.16','image':'http://120.77.36.131/_uploads/images/88x7uv4draw6qs22.png','origin':'2019.2.16'}'
@content.route('/scenery/info/name=<t_name>')
@cache.cached(timeout=300)  # timeout:缓存有效期,默认300s,key_prefix:缓存键前缀,默认:view/+路由地址
def Scenery_info(t_name):
    temp = Scenery.query.filter_by(name=t_name).first()

    return json.dumps(eval(str(temp)), ensure_ascii=False)  # 可用jsonify；ensure_ascii=False解决中文问题


# 上传新景点
@content.route('/scenery/add', methods=['GET', 'POST'])
def Scenery_add():
    form = SceneryForm()
    if request.method == 'POST':
        name = form.name.data
        content = form.content.data
        origin = form.origin.data
        # 获取上传文件
        image = form.images.data
        img_url = upload_image(image)
        if name and content and origin:
            try:
                new_scenery = Scenery(name=name, content=content, image=img_url, origin=origin)
                db.session.add(new_scenery)
                db.session.commit()
                return '上传成功'
            except Exception as e:
                print(e)
                flash('添加景点失败')
                db.session.rollback()
                return '添加失败'
        else:
            return '参数出错'

    return render_template('upload.html', form=form)


# 2.地图导航
# 返回可选类别--返回：json列表
# '{"0": {"id": 1, "name": "书院"},
#   "1": {"id": 2, "name": "上课"},
#   "2": {"id": 3, "name": "活动"},
#   "3": {"id": 4, "name": "餐饮"},
#   "4": {"id": 5, "name": "学院"},
#   "5": {"id": 6, "name": "办公"},
#   "6": {"id": 7, "name": "生活"},
#   "7": {"id": 8, "name": "其他"}}'
@content.route('/place/class/')
@cache.cached(timeout=300)
def Place_class():
    temp = PlaceC.query.all()
    title = [i for i in range(len(temp))]

    # sorted(***)按照id排序字典，确保和title对齐
    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 返回地点列表和具体内容--输入：类别id--返回：json列表
# '{"0": {"id": 1, "name": "至诚书院", "coordinate": "1;1", "placeC_id": 1},
#   "1": {"id": 9, "name": "弘毅书院", "coordinate": "9;9", "placeC_id": 1}}'
@content.route('/place/list/id=<t_id>')
@cache.cached(timeout=300)
def Place_list(t_id):
    temp = Place.query.filter_by(placeC_id=t_id).all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 上传新地点
@content.route('/place/add/', methods=['GET', 'POST'])
def Place_add():
    form = PlaceForm()
    if request.method == 'POST':
        name = form.name.data
        coordinate = form.coordinate.data
        placeC_id = form.placeC_id.data
        if name and coordinate and placeC_id:
            try:
                new_place = Place(name=name, coordinate=coordinate, placeC_id=placeC_id)
                db.session.add(new_place)
                db.session.commit()
                return '上传成功'
            except Exception as e:
                print(e)
                flash('添加地点失败')
                db.session.rollback()
                return '添加失败'
        else:
            return '参数出错'

    return render_template('upload.html', form=form)


# 4.学校其他信息
# 返回信息名称列表--返回：json列表
# '{"1": "校训1",
#   "2": "校训2",
#   "3": "校训3"}'
@content.route('/message/list/')
@cache.cached(timeout=300)
def Message_list():
    temp = Message.query.all()
    dict_name = {}
    for i in range(len(temp)):
        dict_name[temp[i].id] = temp[i].name

    return json.dumps(dict_name, ensure_ascii=False)


# 返回具体信息--输入：名称--返回：具体信息
# '{"id": 1, "name": "校训1", "content": "有志", "image": "None"}'
@content.route('/message/info/name=<t_name>')
@cache.cached(timeout=300)
def Message_info(t_name):
    temp = Message.query.filter_by(name=t_name).first()

    return json.dumps(eval(str(temp)), ensure_ascii=False)


# 5.学校周边
# 周边分类--返回：json列表
# '{"0": {"id": 1, "name": "美食"},
#   "1": {"id": 2, "name": "娱乐"},
#   "2": {"id": 3, "name": "游玩"},
#   "3": {"id": 4, "name": "出行"}}'
@content.route('/play/class/')
@cache.cached(timeout=300)
def Play_class():
    temp = PlayC.query.all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 周边列表--输入：所在的类别，返回所有信息--返回：json列表
# '{"0": {"id": 1, "name": "草莓冰", "content": "草莓冰好吃", "image": null}}'
@content.route('/play/list/class_id=<t_class_id>')
@cache.cached(timeout=300)
def Play_list(t_class_id):
    temp = Play.query.filter_by(playC_id=t_class_id).all()
    list_name = []
    for i in temp:
        dict = {}
        dict['id'] = i.id
        dict['name'] = i.name
        dict['content'] = i.content
        dict['image'] = i.image
        list_name.append(dict)
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(list_name), title), ensure_ascii=False)


# 周边--输入：周边id--返回：具体信息
# '{"id": 1, "name": "草莓冰", "content": "草莓冰好吃", "image": "None", "local": "十二中", "phone": "10086",
#   "origin": "草莓冰", "playC_id": 1}'
@content.route('/play/id=<t_id>')
@cache.cached(timeout=300)
def Play(t_id):
    temp = Play.query.filter_by(id=t_id).first()

    return json.dumps(eval(str(temp)), ensure_ascii=False)


# 上传新周边
@content.route('/play/add/', methods=['GET', 'POST'])
def Play_add():
    form = PlayForm()
    if request.method == 'POST':
        name = form.name.data
        content = form.content.data
        local = form.local.data
        origin = form.origin.data
        playC_id = form.playC_id.data
        image = form.images.data
        img_url = upload_image(image)
        if name and content and local and origin and playC_id:
            try:
                new_play = Play(name=name, content=content, image=img_url, local=local, origin=origin, playC_id=playC_id)
                db.session.add(new_play)
                db.session.commit()
                return '上传成功'
            except Exception as e:
                print(e)
                flash('添加周边失败')
                db.session.rollback()
                return '添加失败'
        else:
            return '参数出错'

    return render_template('upload.html', form=form)


# 问题分类--返回：json列表
# '{"0": {"id": 1, "name": "功能问题"},
#   "1": {"id": 2, "name": "内容问题"}}'
@content.route('/question/class/')
@cache.cached(timeout=300)
def Question_class():
    temp = QuestionC.query.all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 问题内容--返回：json列表
# '{"0": {"id": 1, "name": "地图导航问题", "content": "爱看不看", "questionC_id": 1}}'
@content.route('/question/id=<t_id>')
@cache.cached(timeout=300)
def Question(t_id):
    temp = Question.query.filter_by(questionC_id=t_id).all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 使用帮助分类--返回：json列表
# '{"0": {"id": 1, "name": "功能使用"}, "1": {"id": 2, "name": "内容使用"}}'
@content.route('/use/class/')
@cache.cached(timeout=300)
def Use_class():
    temp = UseC.query.all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 帮助内容
# '{"0": {"id": 1, "name": "景点", "content": "首页点一下", "useC_id": 1}}'
@content.route('/use/id=<t_id>')
@cache.cached(timeout=300)
def Use(t_id):
    temp = Use.query.filter_by(useC_id=t_id).all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)