#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys
import json
import config
from flask import Blueprint
from operator import attrgetter  # 排序操作
from flask import request, flash, render_template
from methods import to_dict, local_time, add_element1, add_element2, upload_image, certify_token

from init import cache, db
from forms import OrganizationMessageCommentForm, OrganizationMessageForm, OrganizationForm
from models import OrganizationC, OrganizationInfo, OrganizationMessage, OrganizationMessageComment

sys.path.append(config.METHODS_PATH)

organizations = Blueprint('organization', __name__)


# 3.学校组织信息
# 返回组织分类--返回：列表
# '{
#   "社团": {"0": {"id": 2, "name": "网球社"}},
#   "组织": {"0": {"id": 1, "name": "学生会"},
#           "1": {"id": 3, "name": "青协"}}
#  }'
@organizations.route('/HelloSTU/organization_class/')
@cache.cached(timeout=300, key_prefix='organization_class')
def organization_class():
    temp = OrganizationC.query.all()
    list_class = []
    list_name = []
    for i in temp:  # 社团，组织  读取一个分类
        list_class.append(i.name)
        a = i.organizationInfo  # 获取相关类别的所有组织内容，返回一个列表
        name = []  # 存储该类别的所有组织相关内容（id+name）
        for j in a:  # 遍历每个分类列表中的每个元素
            dict = {}
            dict['id'] = j.id
            dict['name'] = j.name
            name.append(dict)  # 生成字典堆叠加入列表
        title = [i for i in range(len(name))]  # 编号
        list_name.append(json.dumps(to_dict(name, title), ensure_ascii=False))

    return json.dumps(to_dict(list_name, list_class), ensure_ascii=False)


# 返回对应组织基本信息--输入：组织名--返回：具体信息
# '{"id": 1, "name": "学生会", "content": "学生会", "image": "None", "origin": "学生会", "organizationC_id": "1"}'
@organizations.route('/HelloSTU/organization_info/name=<t_name>')
@cache.cached(timeout=300, key_prefix='organization_info')
def organization_info(t_name):
    temp = OrganizationInfo.query.filter_by(name=t_name).first()

    return json.dumps(eval(str(temp)), ensure_ascii=False)


# 上传新组织
@organizations.route('/HelloSTU/add_organization/', methods=['GET', 'POST'])
def add_organization():
    form = OrganizationForm()
    if request.method == 'POST':
        name = form.name.data
        content = form.content.data
        origin = form.origin.data
        organizationC_id = form.organizationC_id.data
        image = form.images.data
        img_url = upload_image(image)
        if name and content and origin and organizationC_id:
            try:
                new_organization = OrganizationInfo(name=name, content=content, image=img_url, origin=origin, organizationC_id=organizationC_id)
                db.session.add(new_organization)
                db.session.commit()
                return '上传成功'
            except Exception as e:
                print(e)
                flash('添加组织失败')
                db.session.rollback()
                return '添加失败'
        else:
            return '参数出错'

    return render_template('upload.html', form=form)


# 返回组织发布的信息--返回：json列表（注意state和倒序）
# {"0": {"id": 1, "title": "学生会活动1", "createTime": "2019-02-10 17:03:36", "activeTime": "2018-2019", "state": 1,
#        "content": "学生会活动1", "image": "None", "agreeNum": 1, "attachment": "None", "commentNum": 10, "writer_id": 1,
#        "writer_name": "学生会主席"},
#  "1": {"id": 2, "title": "网球社活动1", "createTime": "2019-02-10 17:03:36", "activeTime": "2018-2019", "state": 1,
#        "content": "网球社活动1", "image": "None", "agreeNum": 1, "attachment": "None", "commentNum": 1, "writer_id": 2,
#        "writer_name": "网球社主席"},
#  "2": {"id": 3, "title": "青协活动1", "createTime": "2019-02-10 17:03:36", "activeTime": "2018-2019", "state": 1,
#        "content": "青协活动1", "image": "None", "agreeNum": 1, "attachment": "None", "commentNum": 1, "writer_id": 3,
#        "writer_name": "青协主席"}}
@organizations.route('/HelloSTU/organization_message/page=<page>&pagesize=<pagesize>')
@cache.cached(timeout=300, key_prefix='organization_message')
def organization_message(page, pagesize):  # 先转int
    state1 = OrganizationMessage.query.filter_by(state=1).all()  # 过滤删除的信息
    state1 = sorted(state1, key=attrgetter('id'), reverse=False)  # 过滤后排序
    t_max = len(state1) - int(page)*int(pagesize) - 1  # 倒序获取最高id的位置（list中）
    if t_max < 0:
        return '没有再多消息了'
    t_max_id = state1[t_max].id  # 获取最大id
    t_min = max(t_max - int(pagesize), 0)
    t_min_id = state1[t_min].id  # 获取最小id
    if t_min != 0:
        temp = OrganizationMessage.query.filter(OrganizationMessage.id <= t_max_id, OrganizationMessage.id > t_min_id,
                                                OrganizationMessage.state == 1).all()
    else:
        temp = OrganizationMessage.query.filter(OrganizationMessage.id <= t_max_id, OrganizationMessage.id >= t_min_id,
                                                OrganizationMessage.state == 1).all()
    title = [i for i in range(len(temp))]

    return json.dumps(add_element1(temp, title), ensure_ascii=False)


@organizations.route('/HelloSTU/add_organization_message/', methods=['GET', 'POST'])
def add_organization_message():
    form = OrganizationMessageForm()
    if request.method == 'POST':
        writer_id = form.writer_id.data
        token = form.token.data
        if certify_token(writer_id, token):
            title = form.title.data
            activeTime = form.activeTime.data
            content = form.content.data
            attachment = form.attachment.data
            createTime = local_time()
            image = form.images.data
            img_url = upload_image(image)
            if writer_id and content:
                try:
                    new_organizationMessage = OrganizationMessage(title=title, createTime=createTime, activeTime=activeTime,
                                                                  state=1, content=content, image=img_url, agreeNum=0,
                                                                  attachment=attachment, commentNum=0, writer_id=writer_id)
                    db.session.add(new_organizationMessage)
                    db.session.commit()
                    return '上传成功'
                except Exception as e:
                    print(e)
                    flash('添加组织发布信息失败')
                    db.session.rollback()
                    return '添加失败'
            else:
                return '参数出错'
        else:
            return '登录超时'

    return render_template('upload.html', form=form)


# 返回对应组织发布信息评论--输入对应的文本的id（可能要返回发布者信息和被回复者信息）--返回：json列表
# '{"0": {"id": 1, "state": 1, "createTime": "2019-02-10 17:03:36", "content": "我觉得学生会说得对", "writer_id": 4,
#   "replied_id": -1, "message_id": 1, "writer_name": "宋兵甲", "replied_name": "null"}'
@organizations.route('/HelloSTU/organization_message_comment/id=<t_id>')
@cache.cached(timeout=300, key_prefix='organization_message_comment')
def organization_message_comment(t_id):
    temp = OrganizationMessageComment.query.filter_by(message_id=t_id, state=1).all()

    title = [i for i in range(len(temp))]
    return json.dumps(add_element2(temp, title), ensure_ascii=False)


@organizations.route('/HelloSTU/add_organization_message_comment/', methods=['GET', 'POST'])
def add_organization_message_comment():
    form = OrganizationMessageCommentForm()
    if request.method == 'POST':
        writer_id = form.writer_id.data
        token = form.token.data
        if certify_token(writer_id, token):
            createTime = local_time()
            content = form.content.data
            replied_id = form.replied_id.data
            message_id = form.message_id.data
            if content and replied_id and message_id:
                try:
                    new_organizationMessageComment = OrganizationMessageComment(state=1, createTime=createTime, content=content,
                                                                                writer_id=writer_id, replied_id=replied_id,
                                                                                message_id=message_id)
                    db.session.add(new_organizationMessageComment)
                    db.session.commit()
                    organizationMessage = OrganizationMessage.query.filter_by(id=message_id).first()  # 评论数+1
                    organizationMessage.commentNum += 1
                    db.session.commit()
                    return '上传成功'
                except Exception as e:
                    print(e)
                    flash('添加组织发布信息评论失败')
                    db.session.rollback()
                    return '添加失败'
            else:
                return '参数出错'
        else:
            return '登录超时'

    return render_template('upload.html', form=form)