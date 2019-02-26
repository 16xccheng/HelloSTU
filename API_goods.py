#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys
import json
import config
from flask import Blueprint
from operator import attrgetter  # 排序操作
from flask import request, flash, render_template
from methods import to_dict, local_time, add_element2, upload_image, certify_token

from init import cache, db
from forms import GoodsCommentForm, GoodsForm
from models import GoodsC, Goods, GoodsComment

sys.path.append(config.METHODS_PATH)

goods = Blueprint('API_goods', __name__)


# 7.二手交易
# 物品分类--返回：json列表
# '{"0": {"id": 1, "name": "生活用品"},
#   "1": {"id": 2, "name": "学习用品"},
#   "2": {"id": 3, "name": "饮食用品"},
#   "3": {"id": 4, "name": "娱乐用品"}}'
@goods.route('/HelloSTU/goods_class/')
@cache.cached(timeout=300, key_prefix='goods_class')
def goods_class():
    temp = GoodsC.query.all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 物品列表--返回：json列表
# '{"0": {"id": 1, "name": "音响", "createTime": "2018-1-31 13:31:13", "image": null},
#   "1": {"id": 2, "name": "高数", "createTime": "2018-1-31 13:31:13", "image": null},
#   "2": {"id": 3, "name": "筷子", "createTime": "2018-1-31 13:31:13", "image": null},
#   "3": {"id": 4, "name": "手柄", "createTime": "2018-1-31 13:31:13", "image": null}}'
@goods.route('/HelloSTU/goods_list/page=<page>&pagesize=<pagesize>')
@cache.cached(timeout=300, key_prefix='goods_list')
def goods_list(page, pagesize):
    state1 = Goods.query.filter_by(state=1).all()
    state1 = sorted(state1, key=attrgetter('id'), reverse=False)
    t_max = len(state1) - int(page)*int(pagesize) - 1
    if t_max < 0:
        return '没有再多物品了'
    t_max_id = state1[t_max].id
    t_min = max(t_max-int(pagesize), 0)
    t_min_id = state1[t_min].id
    if t_min != 0:
        temp = Goods.query.filter(Goods.id <= t_max_id, Goods.id > t_min_id, Goods.state == 1).all()
    else:
        temp = Goods.query.filter(Goods.id <= t_max_id, Goods.id >= t_min_id, Goods.state == 1).all()
    list_name = []
    for i in temp:
        dict = {}
        dict['id'] = i.id
        dict['name'] = i.name
        dict['createTime'] = i.createTime
        dict['image'] = i.image
        list_name.append(dict)
    title = [i for i in range(len(list_name))]

    return json.dumps(to_dict(list_name, title), ensure_ascii=False)


# 物品详情--输入：物品id--返回：具体信息
# '{"id": 1, "name": "音响", "createTime": "2018-1-31 13:31:13", "state": 1, "price": 999, "content": "音响",
#   "image": "None", "phone": "10086", "wechat": "None", "email": "None", "commentNum": 1, "writer_id": 1,
#   "type": "生活用品"}'
@goods.route('/HelloSTU/goods/id=<t_id>')
@cache.cached(timeout=300, key_prefix='goods')
def _goods(t_id):
    temp = Goods.query.filter_by(id=t_id).first()

    return json.dumps(eval(str(temp)), ensure_ascii=False)


# 上传新商品
@goods.route('/HelloSTU/add_goods/', methods=['GET', 'POST'])
def add_goods():
    form = GoodsForm()
    if request.method == 'POST':
        writer_id = form.writer_id.data
        token = form.token.data
        if certify_token(writer_id, token):
            name = form.name.data
            price = form.price.data
            content = form.content.data
            phone = form.phone.data
            wechat = form.wechat.data
            email = form.email.data
            type = form.type.data
            createTime = local_time()
            state = 1
            commentNum = 0
            image = form.images.data
            img_url = upload_image(image)
            if name and price and content and type:
                try:
                    new_goods = Goods(name=name, createTime=createTime, state=state, price=price, content=content,
                                      image=img_url, phone=phone, wechat=wechat, email=email, commentNum=commentNum,
                                      writer_id=writer_id, type=type)

                    db.session.add(new_goods)
                    db.session.commit()
                    return '上传成功'
                except Exception as e:
                    print(e)
                    flash('添加商品失败')
                    db.session.rollback()
                    return '添加失败'
            else:
                return '参数出错'
        else:
            return '登录超时'

    return render_template('upload.html', form=form)


# 物品评论--输入：物品id--返回：json列表
# {"0": {"id": 1, "state": 1, "createTime": "2019-02-10 17:03:36", "content": "我觉得这是1手的", "writer_id": 2,
#  "replied_id": -1, "goods_id": 1, "writer_name": "网球社主席", "replied_name": "null"}}
@goods.route('/HelloSTU/goods_comment/id=<t_id>')
@cache.cached(timeout=300, key_prefix='goods_comment')
def goods_comment(t_id):
    temp = GoodsComment.query.filter_by(goods_id=t_id, state=1).all()
    title = [i for i in range(len(temp))]

    return json.dumps(add_element2(temp, title), ensure_ascii=False)


@goods.route('/HelloSTU/add_goods_comment/', methods=['GET', 'POST'])
def add_goods_comment():
    form = GoodsCommentForm()
    if request.method == 'POST':
        writer_id = form.writer_id.data
        token = form.token.data
        if certify_token(writer_id, token):
            createTime = local_time()
            content = form.content.data
            replied_id = form.replied_id.data
            goods_id = form.goods_id.data
            if content and replied_id and goods_id:
                try:
                    new_goodsComment = GoodsComment(state=1, createTime=createTime, content=content,
                                                              writer_id=writer_id, replied_id=replied_id,
                                                              goods_id=goods_id)
                    db.session.add(new_goodsComment)
                    db.session.commit()
                    goods = Goods.query.filter_by(id=goods_id).first()  # 评论数+1
                    goods.commentNum += 1
                    db.session.commit()
                    return '上传成功'
                except Exception as e:
                    print(e)
                    flash('添加物品评论失败')
                    db.session.rollback()
                    return '添加失败'
            else:
                return '参数出错'
        else:
            return '登录超时'

    return render_template('upload.html', form=form)