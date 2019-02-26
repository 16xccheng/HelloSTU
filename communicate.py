#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys
import json
import config
from flask import Blueprint
from operator import attrgetter  # 排序操作
from flask import request, flash, render_template

from init import cache, db
from models import UsrMessage, UsrMessageComment
from forms import UsrMessageForm, UsrMessageCommentForm
from methods import local_time, add_element1, add_element2, upload_image, certify_token

sys.path.append(config.METHODS_PATH)

communicates = Blueprint('communicate', __name__)


# 6.社交圈子
# 用户发布信息列表(可改一次发送10条)--返回：json列表
# {"0": {"id": 1, "createTime": "2019-02-10 17:03:36", "content": "我说1", "image": "None", "agreeNum": 1,
#        "commentNum": 1, "state": 1, "writer_id": 1, "writer_name": "学生会主席"},
#  "1": {"id": 2, "createTime": "2019-02-10 17:03:36", "content": "我说2", "image": "None", "agreeNum": 2,
#        "commentNum": 1, "state": 1, "writer_id": 2, "writer_name": "网球社主席"},
#  "2": {"id": 3, "createTime": "2019-02-10 17:03:36", "content": "我说3", "image": "None", "agreeNum": 3,
#        "commentNum": 1, "state": 1, "writer_id": 3, "writer_name": "青协主席"}}
@communicates.route('/HelloSTU/usr_message/page=<page>&pagesize=<pagesize>')
@cache.cached(timeout=300, key_prefix='usr_message')
def usr_message(page, pagesize):
    state1 = UsrMessage.query.filter_by(state=1).all()
    state1 = sorted(state1, key=attrgetter('id'), reverse=False)
    t_max = len(state1) - int(page)*int(pagesize) - 1
    if t_max < 0:
        return '没有再多消息了'
    t_max_id = state1[t_max].id
    t_min = max(t_max - int(pagesize), 0)
    t_min_id = state1[t_min].id
    if t_min != 0:
        temp = UsrMessage.query.filter(UsrMessage.id <= t_max_id, UsrMessage.id > t_min_id, UsrMessage.state == 1).all()
    else:
        temp = UsrMessage.query.filter(UsrMessage.id <= t_max_id, UsrMessage.id >= t_min_id, UsrMessage.state == 1).all()
    title = [i for i in range(len(temp))]

    return json.dumps(add_element1(temp, title), ensure_ascii=False)


@communicates.route('/HelloSTU/add_usr_message/', methods=['GET', 'POST'])
def add_usr_message():
    form = UsrMessageForm()
    if request.method == 'POST':
        writer_id = form.writer_id.data
        token = form.token.data
        if certify_token(writer_id, token):
            content = form.content.data
            createTime = local_time()
            image = form.images.data
            img_url = upload_image(image)
            if content:
                try:
                    new_UsrMessage = UsrMessage(createTime=createTime, state=1, content=content, image=img_url, agreeNum=0,
                                                commentNum=0, writer_id=writer_id)
                    db.session.add(new_UsrMessage)
                    db.session.commit()
                    return '上传成功'
                except Exception as e:
                    print(e)
                    flash('添加用户发布信息失败')
                    db.session.rollback()
                    return '添加失败'
            else:
                return '参数出错'
        else:
            return '登录超时'

    return render_template('upload.html', form=form)


# 用户发布信息评论--输入：信息对应id--返回：json列表
# {"0": {"id": 1, "createTime": "2019-02-10 17:03:36", "content": "我说1说得对", "state": 1, "writer_id": 4,
#        "replied_id": -1, "message_id": 1, "writer_name": "宋兵甲", "replied_name": "null"}}
@communicates.route('/HelloSTU/usr_message_comment/id=<t_id>')
@cache.cached(timeout=300, key_prefix='usr_message_comment')
def usr_message_comment(t_id):
    temp = UsrMessageComment.query.filter_by(message_id=t_id, state=1).all()
    title = [i for i in range(len(temp))]

    return json.dumps(add_element2(temp, title), ensure_ascii=False)


@communicates.route('/HelloSTU/add_usr_message_comment/', methods=['GET', 'POST'])
def add_usr_message_comment():
    form = UsrMessageCommentForm()
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
                    new_usrMessageComment = UsrMessageComment(state=1, createTime=createTime, content=content,
                                                              writer_id=writer_id, replied_id=replied_id,
                                                              message_id=message_id)
                    db.session.add(new_usrMessageComment)
                    db.session.commit()
                    usrMessage = UsrMessage.query.filter_by(id=message_id).first()  # 评论数+1
                    usrMessage.commentNum += 1
                    db.session.commit()
                    return '上传成功'
                except Exception as e:
                    print(e)
                    flash('添加用户发布信息评论失败')
                    db.session.rollback()
                    return '添加失败'
            else:
                return '参数出错'
        else:
            return '登录超时'

    return render_template('upload.html', form=form)