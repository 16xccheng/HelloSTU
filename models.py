#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import hmac

from init import db


# #################################################### 表单类大小 ##################################################### #
passwordSize = 256  # 密码
contentSize = 256  # 文本
imageSize = 256  # 图片路径

activeTimeSize = 64  # 活动时间
attachmentSize = 64  # 附件链接

createTimeSize = 32  # 创建时间
localSize = 32  # 地址
emailSize = 32  # 邮件

coordinateSize = 16  # 坐标
permissionSize = 16  # 权限
accountSize = 16  # 账号
originSize = 16  # 来源
wechatSize = 16  # 微信
writerSize = 16  # 作者
phoneSize = 16  # 电话
titleSize = 16  # 标题
typeSize = 16  # 类型
nameSize = 16  # 名字


# #################################################### 数据库表单 ##################################################### #
# 1.景点介绍
# 景点
class Scenery(db.Model):
    __tablename__ = 'sceneries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    content = db.Column(db.String(contentSize))
    image = db.Column(db.String(imageSize))
    origin = db.Column(db.String(originSize))

    # 打印
    def __repr__(self):
        return "{'id':%d,'name':'%s','content':'%s','image':'%s','origin':'%s'}" \
               % (self.id, self.name, self.content, self.image, self.origin)


# 2.地图导航
# 地图分类
class PlaceC(db.Model):
    __tablename__ = 'placeCs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    place = db.relationship('Place', backref='placeC')

    def __repr__(self):
        return "{'id':%d,'name':'%s'}" \
               % (self.id, self.name)


# 地点
class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    coordinate = db.Column(db.String(coordinateSize))
    placeC_id = db.Column(db.Integer, db.ForeignKey('placeCs.id'))

    def __repr__(self):
        return "{'id':%d,'name':'%s','coordinate':'%s','placeC_id':%d}" \
               % (self.id, self.name, self.coordinate, self.placeC_id)


# 3.学校组织信息
# # 组织分类
class OrganizationC(db.Model):
    __tablename__ = 'organizationCs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    organizationInfo = db.relationship('OrganizationInfo', backref='organizationC')

    def __repr__(self):
        return "{'id':%d,'name':'%s'}" \
               % (self.id, self.name)


# 组织基本信息
class OrganizationInfo(db.Model):
    __tablename__ = 'organizationInfos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    content = db.Column(db.String(contentSize))
    image = db.Column(db.String(imageSize))
    origin = db.Column(db.String(originSize))
    organizationC_id = db.Column(db.Integer, db.ForeignKey('organizationCs.id'))

    def __repr__(self):
        return "{'id':%d,'name':'%s','content':'%s','image':'%s','origin':'%s','organizationC_id':'%s'}" \
               % (self.id, self.name, self.content, self.image, self.origin, self.organizationC_id)


# 组织发布的信息
class OrganizationMessage(db.Model):
    __tablename__ = 'organizationMessages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(titleSize))
    createTime = db.Column(db.String(createTimeSize))
    activeTime = db.Column(db.String(activeTimeSize))
    state = db.Column(db.Integer)  # 状态（是否删除）
    content = db.Column(db.String(contentSize))
    image = db.Column(db.String(imageSize))
    agreeNum = db.Column(db.Integer)  # 点赞数
    attachment = db.Column(db.String(attachmentSize))
    commentNum = db.Column(db.Integer)
    writer_id = db.Column(db.Integer)
    organizationMessageComment = db.relationship('OrganizationMessageComment', backref='organizationMessage')

    def __repr__(self):
        return "{'id':%d,'title':'%s','createTime':'%s','activeTime':'%s','state':%d,'content':'%s','image':'%s', 'agreeNum':%d,'attachment':'%s','commentNum':%d,'writer_id':%d}" \
               % (self.id, self.title, self.createTime, self.activeTime, self.state, self.content, self.image,
                  self.agreeNum, self.attachment, self.commentNum, self.writer_id)


# 组织发布信息评论
class OrganizationMessageComment(db.Model):
    __tablename__ = 'organizationMessageComments'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Integer)  # 状态（是否删除）
    createTime = db.Column(db.String(createTimeSize))
    content = db.Column(db.String(contentSize))
    writer_id = db.Column(db.Integer)  # 发布者id
    replied_id = db.Column(db.Integer)  # 回复的评论的作者id
    message_id = db.Column(db.Integer, db.ForeignKey('organizationMessages.id'))  # 对应信息的id

    def __repr__(self):
        return "{'id':%d,'state':%d,'createTime':'%s','content':'%s','writer_id':%d,'replied_id':%d,'message_id':%d}" \
               % (self.id, self.state, self.createTime, self.content, self.writer_id, self.replied_id, self.message_id)


# 4.学校其他信息
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    content = db.Column(db.String(contentSize))
    image = db.Column(db.String(imageSize))

    def __repr__(self):
        return "{'id':%d,'name':'%s','content':'%s','image':'%s'}" \
               % (self.id, self.name, self.content, self.image)


# 5.学校周边
# 周边分类
class PlayC(db.Model):
    __tablename__ = 'playCs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    play = db.relationship('Play', backref='playC')

    def __repr__(self):
        return "{'id':%d,'name':'%s'}" \
               % (self.id, self.name)


# 周边
class Play(db.Model):
    __tablename__ = 'plays'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    content = db.Column(db.String(contentSize))
    image = db.Column(db.String(imageSize))
    local = db.Column(db.String(localSize))
    phone = db.Column(db.String(phoneSize))
    origin = db.Column(db.String(originSize))
    playC_id = db.Column(db.Integer, db.ForeignKey('playCs.id'))

    def __repr__(self):
        return "{'id':%d,'name':'%s','content':'%s','image':'%s','local':'%s','phone':'%s','origin':'%s','playC_id':%d}" \
               % (self.id, self.name, self.content, self.image, self.local, self.phone, self.origin, self.playC_id)


# 6.社交圈子
# 用户发布信息
class UsrMessage(db.Model):
    __tablename__ = 'usrMessages'
    id = db.Column(db.Integer, primary_key=True)
    createTime = db.Column(db.String(createTimeSize))
    content = db.Column(db.String(contentSize))
    image = db.Column(db.String(imageSize))
    agreeNum = db.Column(db.Integer)  # 点赞数
    commentNum = db.Column(db.Integer)  # 评论数
    state = db.Column(db.Integer)  # 状态（是否删除）
    writer_id = db.Column(db.Integer)
    usrMessageComment = db.relationship('UsrMessageComment', backref='usrMessage')

    def __repr__(self):
        return "{'id':%d,'createTime':'%s','content':'%s','image':'%s','agreeNum':%d,'commentNum':%d,'state':%d, 'writer_id':%d}" \
               % (self.id, self.createTime, self.content, self.image, self.agreeNum, self.commentNum, self.state,
                  self.writer_id)


# 用户发布信息评论
class UsrMessageComment(db.Model):
    __tablename__ = 'usrMessageComments'
    id = db.Column(db.Integer, primary_key=True)
    createTime = db.Column(db.String(createTimeSize))
    content = db.Column(db.String(contentSize))
    state = db.Column(db.Integer)  # 状态（是否删除）
    writer_id = db.Column(db.Integer)  # 发布者id
    replied_id = db.Column(db.Integer)  # 回复的评论的作者id
    message_id = db.Column(db.Integer, db.ForeignKey('usrMessages.id'))  # 对应信息的id

    def __repr__(self):
        return "{'id':%d,'createTime':'%s','content':'%s','state':%d,'writer_id':%d,'replied_id':%d,'message_id':%d}" \
               % (self.id, self.createTime, self.content, self.state, self.writer_id, self.replied_id, self.message_id)


# 7.二手交易
# 物品分类
class GoodsC(db.Model):
    __tablename__ = 'goodsCs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)

    def __repr__(self):
        return "{'id':%d,'name':'%s'}" \
               % (self.id, self.name)


# 物品
class Goods(db.Model):
    __tablename__ = 'goodss'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize))
    createTime = db.Column(db.String(createTimeSize))
    state = db.Column(db.Integer)  # 状态（是否删除）
    price = db.Column(db.Integer)
    content = db.Column(db.String(contentSize))
    image = db.Column(db.String(imageSize))
    phone = db.Column(db.String(phoneSize))
    wechat = db.Column(db.String(wechatSize))
    email = db.Column(db.String(emailSize))
    commentNum = db.Column(db.Integer)
    writer_id = db.Column(db.Integer)  # 商家账号id
    type = db.Column(db.String(typeSize))
    goodsComment = db.relationship('GoodsComment', backref='goods')

    def __repr__(self):
        return "{'id':%d,'name':'%s','createTime':'%s','state':%d,'price':%d,'content':'%s','image':'%s','phone':'%s', 'wechat':'%s','email':'%s','commentNum':%d,'writer_id':%d,'type':'%s'}" \
               % (self.id, self.name, self.createTime, self.state, self.price, self.content, self.image, self.phone,
                  self.wechat, self.email, self.commentNum, self.writer_id, self.type)


# 物品评论
class GoodsComment(db.Model):
    __tablename__ = 'goodsComments'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Integer)  # 状态（是否删除）
    createTime = db.Column(db.String(createTimeSize))
    content = db.Column(db.String(contentSize))
    writer_id = db.Column(db.Integer)  # 发布者id
    replied_id = db.Column(db.Integer)  # 回复的评论的作者id
    goods_id = db.Column(db.Integer, db.ForeignKey('goodss.id'))  # 对应商品的id

    def __repr__(self):
        return "{'id':%d,'state':%d,'createTime':'%s','content':'%s','writer_id':%d,'replied_id':%d,'goods_id':%d}" \
               % (self.id, self.state, self.createTime, self.content, self.writer_id, self.replied_id, self.goods_id)


# 8.我的
# 基本信息
class UsrInfo(db.Model):
    __tablename__ = 'usrInfos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize))
    account = db.Column(db.String(accountSize), unique=True)
    password = db.Column(db.String(passwordSize))
    permission = db.Column(db.String(permissionSize))

    def hash_password(self, passWord):  # 给密码加密方法
        h = hmac.new('HelloSTU'.encode('utf-8'))
        h.update(passWord.encode('utf-8'))
        self.password = h.hexdigest()

    def verify_password(self, passWord):  # 验证密码方法
        h = hmac.new('HelloSTU'.encode('utf-8'))
        h.update(passWord.encode('utf-8'))
        passWord = h.hexdigest()
        return passWord == self.password

    def __repr__(self):
        return "{'id':%d,'name':'%s','account':'%s','password':'%s','permission':'%s'}" \
               % (self.id, self.name, self.account, self.password, self.permission)


# 问题分类
class QuestionC(db.Model):
    __tablename__ = 'questionCs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    question = db.relationship('Question', backref='questionC')

    def __repr__(self):
        return "{'id':%d,'name':'%s'}" \
               % (self.id, self.name)


# 问题
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    content = db.Column(db.String(contentSize))
    questionC_id = db.Column(db.Integer, db.ForeignKey('questionCs.id'))

    def __repr__(self):
        return "{'id':%d,'name':'%s','content':'%s','questionC_id':%d}" \
               % (self.id, self.name, self.content, self.questionC_id)


# 使用帮助分类
class UseC(db.Model):
    __tablename__ = 'useCs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    use = db.relationship('Use', backref='useC')

    def __repr__(self):
        return "{'id':%d,'name':'%s'}" \
               % (self.id, self.name)


# 使用帮助
class Use(db.Model):
    __tablename__ = 'uses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(nameSize), unique=True)
    content = db.Column(db.String(contentSize))
    useC_id = db.Column(db.Integer, db.ForeignKey('useCs.id'))

    def __repr__(self):
        return "{'id':%d,'name':'%s','content':'%s','useC_id':%d}" \
               % (self.id, self.name, self.content, self.useC_id)