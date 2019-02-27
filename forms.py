#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired

from init import images


# ###################################################### 上传表单 ##################################################### #
# 景点
class SceneryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    images = FileField('images', validators=[FileRequired(message='choose an image'), FileAllowed(images)])
    origin = StringField('origin', validators=[DataRequired()])
    submit = SubmitField('submit')


# 地点
class PlaceForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    coordinate = StringField('coordinate', validators=[DataRequired()])
    placeC_id = IntegerField('placeC_id', validators=[DataRequired()])
    submit = SubmitField('submit')


# 组织
class OrganizationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    images = FileField('images', validators=[FileRequired(message='choose an image'), FileAllowed(images)])
    origin = StringField('origin', validators=[DataRequired()])
    organizationC_id = IntegerField('organizationC_id', validators=[DataRequired()])
    submit = SubmitField('submit')


# 组织信息
class OrganizationMessageForm(FlaskForm):
    writer_id = IntegerField('writer_id', validators=[DataRequired()])
    # token = StringField('token', validators=[DataRequired()])
    rdSession = StringField('rdSession', validators=[DataRequired()])  #
    title = StringField('title', validators=[DataRequired()])
    activeTime = StringField('activeTime', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    images = FileField('images', validators=[FileRequired(message='choose an image'), FileAllowed(images)])
    attachment = StringField('attachment', validators=[DataRequired()])
    submit = SubmitField('submit')


# 组织信息评论
class OrganizationMessageCommentForm(FlaskForm):
    writer_id = IntegerField('writer_id', validators=[DataRequired()])
    # token = StringField('token', validators=[DataRequired()])
    rdSession = StringField('rdSession', validators=[DataRequired()])  #
    content = StringField('content', validators=[DataRequired()])
    replied_id = IntegerField('replied_id', validators=[DataRequired()])
    message_id = IntegerField('message_id', validators=[DataRequired()])
    submit = SubmitField('submit')


# 周边
class PlayForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    images = FileField('images', validators=[FileRequired(message='choose an image'), FileAllowed(images)])
    local = StringField('local', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    origin = StringField('origin', validators=[DataRequired()])
    playC_id = IntegerField('playC_id', validators=[DataRequired()])
    submit = SubmitField('submit')


# 社交信息
class UsrMessageForm(FlaskForm):
    writer_id = IntegerField('writer_id', validators=[DataRequired()])
    # token = StringField('token', validators=[DataRequired()])
    rdSession = StringField('rdSession', validators=[DataRequired()])  #
    content = StringField('content', validators=[DataRequired()])
    images = FileField('images', validators=[FileRequired(message='choose an image'), FileAllowed(images)])
    submit = SubmitField('submit')


# 社交信息评论
class UsrMessageCommentForm(FlaskForm):
    writer_id = IntegerField('writer_id', validators=[DataRequired()])
    # token = StringField('token', validators=[DataRequired()])
    rdSession = StringField('rdSession', validators=[DataRequired()])  #
    content = StringField('content', validators=[DataRequired()])
    replied_id = IntegerField('replied_id', validators=[DataRequired()])
    message_id = IntegerField('message_id', validators=[DataRequired()])
    submit = SubmitField('submit')


# 商品
class GoodsForm(FlaskForm):
    writer_id = IntegerField('writer_id', validators=[DataRequired()])
    # token = StringField('token', validators=[DataRequired()])
    rdSession = StringField('rdSession', validators=[DataRequired()])  #
    name = StringField('name', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    images = FileField('images', validators=[FileRequired(message='choose an image'), FileAllowed(images)])
    phone = StringField('phone', validators=[DataRequired()])
    wechat = StringField('wechat', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    type = StringField('type', validators=[DataRequired()])
    submit = SubmitField('submit')


# 商品评论
class GoodsCommentForm(FlaskForm):
    writer_id = IntegerField('writer_id', validators=[DataRequired()])
    # token = StringField('token', validators=[DataRequired()])
    rdSession = StringField('rdSession', validators=[DataRequired()]) #
    content = StringField('content', validators=[DataRequired()])
    replied_id = IntegerField('replied_id', validators=[DataRequired()])
    goods_id = IntegerField('goods_id', validators=[DataRequired()])
    submit = SubmitField('submit')


# 用户注册
class UsrRegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    account = StringField('account', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('submit')


# 用户登录
class UsrLoginForm(FlaskForm):
    account = StringField('account', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('submit')


# 小程序用户登录
class WxLoginForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    submit = SubmitField('submit')


# 小程序用户信息更新
class WxUpdateForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    rdSession = StringField('rdSession', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    image = StringField('image', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('submit')