# #####################################################################################################################
# 名称：HelloSTU后端主程序
# 作者：程晓聪
# 版本：1.0
# 修改：2019.2.10
# #####################################################################################################################


# -*- coding:utf-8 -*-
from flask import Flask, request, flash, render_template  # jsonify
from flask_sqlalchemy import SQLAlchemy
from operator import attrgetter  # 排序操作
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES, configure_uploads
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap  # 文件拓展
from flask_script import Manager  # 文件拓展
from flask_cache import Cache
import os
import time
import base64
import hmac
import json
import random
import config


app = Flask(__name__)
# 配置缓存
cache = Cache(app, config={
    "CACHE_TYPE": "redis",  # 类型
    "CACHE_REDIS_HOST": "127.0.0.1",  # 主机
    "CACHE_REDIS_PORT": 6379,  # 端口
    "CACHE_REDIS_PASSWORD": "ljgljgljg",  # 密码
    "CACHE_REDIS_DB": 16  # 数据库
})

# 设置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
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
app.secret_key = config.secret_key


# 创建数据库对象
db = SQLAlchemy(app)
# 文件（图片）拓展
manager = Manager(app)
bootstrap = Bootstrap(app)


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


# #################################################### 表单类大小 ##################################################### #
passwordSize = 256    # 密码
contentSize = 256    # 文本
imageSize = 256      # 图片路径

activeTimeSize = 64  # 活动时间
attachmentSize = 64  # 附件链接

createTimeSize = 32  # 创建时间
localSize = 32       # 地址
emailSize = 32       # 邮件

coordinateSize = 16  # 坐标
permissionSize = 16  # 权限
accountSize = 16     # 账号
originSize = 16      # 来源
wechatSize = 16      # 微信
writerSize = 16      # 作者
phoneSize = 16       # 电话
titleSize = 16       # 标题
typeSize = 16        # 类型
nameSize = 16        # 名字


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
               % (self.id, self.title, self.createTime, self.activeTime, self.state, self.content, self.image, self.agreeNum, self.attachment, self.commentNum, self.writer_id)


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
        return "{'id':%d,'name':'%s','content':'%s','image':'%s','local':'%s','phone':'%s','origin':'%s','playC_id':%d}"\
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
               % (self.id, self.createTime, self.content, self.image, self.agreeNum, self.commentNum, self.state, self.writer_id)


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
               % (self.id, self.name, self.createTime, self.state, self.price, self.content, self.image, self.phone, self.wechat, self.email, self.commentNum, self.writer_id, self.type)


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
    token = StringField('token', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    activeTime = StringField('activeTime', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    images = FileField('images', validators=[FileRequired(message='choose an image'), FileAllowed(images)])
    attachment = StringField('attachment', validators=[DataRequired()])
    submit = SubmitField('submit')


# 组织信息评论
class OrganizationMessageCommentForm(FlaskForm):
    writer_id = IntegerField('writer_id', validators=[DataRequired()])
    token = StringField('token', validators=[DataRequired()])
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
    token = StringField('token', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    images = FileField('images', validators=[FileRequired(message='choose an image'), FileAllowed(images)])
    submit = SubmitField('submit')


# 社交信息评论
class UsrMessageCommentForm(FlaskForm):
    writer_id = IntegerField('writer_id', validators=[DataRequired()])
    token = StringField('token', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    replied_id = IntegerField('replied_id', validators=[DataRequired()])
    message_id = IntegerField('message_id', validators=[DataRequired()])
    submit = SubmitField('submit')


# 商品
class GoodsForm(FlaskForm):
    writer_id = IntegerField('writer_id', validators=[DataRequired()])
    token = StringField('token', validators=[DataRequired()])
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
    token = StringField('token', validators=[DataRequired()])
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


# ###################################################### 请求发送 ##################################################### #
# 1.景点
# 请求景点信息--输入：名称--返回：具体信息
# '{'id':6,'name':'2019.2.16','content':'2019.2.16','image':'http://120.77.36.131/_uploads/images/88x7uv4draw6qs22.png','origin':'2019.2.16'}'
@app.route('/HelloSTU/scenery_info/name=<t_name>')
@cache.cached(timeout=300, key_prefix='scenery_info')  # timeout:缓存有效期,默认300s,key_prefix:缓存键前缀,默认:view/+路由地址
def scenery_info(t_name):
    temp = Scenery.query.filter_by(name=t_name).first()

    return json.dumps(eval(str(temp)), ensure_ascii=False)  # 可用jsonify；ensure_ascii=False解决中文问题


# 上传新景点
@app.route('/HelloSTU/add_scenery/', methods=['GET', 'POST'])
def add_scenery():
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
@app.route('/HelloSTU/place_class/')
@cache.cached(timeout=300, key_prefix='place_class')
def place_class():
    temp = PlaceC.query.all()
    title = [i for i in range(len(temp))]

    # sorted(***)按照id排序字典，确保和title对齐
    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 返回地点列表和具体内容--输入：类别id--返回：json列表
# '{"0": {"id": 1, "name": "至诚书院", "coordinate": "1;1", "placeC_id": 1},
#   "1": {"id": 9, "name": "弘毅书院", "coordinate": "9;9", "placeC_id": 1}}'
@app.route('/HelloSTU/place_list/id=<t_id>')
@cache.cached(timeout=300, key_prefix='place_list')
def place_list(t_id):
    temp = Place.query.filter_by(placeC_id=t_id).all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 上传新地点
@app.route('/HelloSTU/add_place/', methods=['GET', 'POST'])
def add_place():
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


# 3.学校组织信息
# 返回组织分类--返回：列表
# '{
#   "社团": {"0": {"id": 2, "name": "网球社"}},
#   "组织": {"0": {"id": 1, "name": "学生会"},
#           "1": {"id": 3, "name": "青协"}}
#  }'
@app.route('/HelloSTU/organization_class/')
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
@app.route('/HelloSTU/organization_info/name=<t_name>')
@cache.cached(timeout=300, key_prefix='organization_info')
def organization_info(t_name):
    temp = OrganizationInfo.query.filter_by(name=t_name).first()

    return json.dumps(eval(str(temp)), ensure_ascii=False)


# 上传新组织
@app.route('/HelloSTU/add_organization/', methods=['GET', 'POST'])
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
@app.route('/HelloSTU/organization_message/page=<page>&pagesize=<pagesize>')
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


@app.route('/HelloSTU/add_organization_message/', methods=['GET', 'POST'])
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
@app.route('/HelloSTU/organization_message_comment/id=<t_id>')
@cache.cached(timeout=300, key_prefix='organization_message_comment')
def organization_message_comment(t_id):
    temp = OrganizationMessageComment.query.filter_by(message_id=t_id, state=1).all()

    title = [i for i in range(len(temp))]
    return json.dumps(add_element2(temp, title), ensure_ascii=False)


@app.route('/HelloSTU/add_organization_message_comment/', methods=['GET', 'POST'])
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


# 4.学校其他信息
# 返回信息名称列表--返回：json列表
# '{"1": "校训1",
#   "2": "校训2",
#   "3": "校训3"}'
@app.route('/HelloSTU/message_list/')
@cache.cached(timeout=300, key_prefix='message_list')
def message_list():
    temp = Message.query.all()
    dict_name = {}
    for i in range(len(temp)):
        dict_name[temp[i].id] = temp[i].name

    return json.dumps(dict_name, ensure_ascii=False)


# 返回具体信息--输入：名称--返回：具体信息
# '{"id": 1, "name": "校训1", "content": "有志", "image": "None"}'
@app.route('/HelloSTU/message_info/name=<t_name>')
@cache.cached(timeout=300, key_prefix='message_info')
def message_info(t_name):
    temp = Message.query.filter_by(name=t_name).first()

    return json.dumps(eval(str(temp)), ensure_ascii=False)


# 5.学校周边
# 周边分类--返回：json列表
# '{"0": {"id": 1, "name": "美食"},
#   "1": {"id": 2, "name": "娱乐"},
#   "2": {"id": 3, "name": "游玩"},
#   "3": {"id": 4, "name": "出行"}}'
@app.route('/HelloSTU/play_class/')
@cache.cached(timeout=300, key_prefix='play_class')
def play_class():
    temp = PlayC.query.all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 周边列表--输入：所在的类别，返回所有信息--返回：json列表
# '{"0": {"id": 1, "name": "草莓冰", "content": "草莓冰好吃", "image": null}}'
@app.route('/HelloSTU/play_list/class_id=<t_class_id>')
@cache.cached(timeout=300, key_prefix='play_list')
def play_list(t_class_id):
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
@app.route('/HelloSTU/play/id=<t_id>')
@cache.cached(timeout=300, key_prefix='play')
def play(t_id):
    temp = Play.query.filter_by(id=t_id).first()

    return json.dumps(eval(str(temp)), ensure_ascii=False)


# 上传新周边
@app.route('/HelloSTU/add_play/', methods=['GET', 'POST'])
def add_play():
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


# 6.社交圈子
# 用户发布信息列表(可改一次发送10条)--返回：json列表
# {"0": {"id": 1, "createTime": "2019-02-10 17:03:36", "content": "我说1", "image": "None", "agreeNum": 1,
#        "commentNum": 1, "state": 1, "writer_id": 1, "writer_name": "学生会主席"},
#  "1": {"id": 2, "createTime": "2019-02-10 17:03:36", "content": "我说2", "image": "None", "agreeNum": 2,
#        "commentNum": 1, "state": 1, "writer_id": 2, "writer_name": "网球社主席"},
#  "2": {"id": 3, "createTime": "2019-02-10 17:03:36", "content": "我说3", "image": "None", "agreeNum": 3,
#        "commentNum": 1, "state": 1, "writer_id": 3, "writer_name": "青协主席"}}
@app.route('/HelloSTU/usr_message/page=<page>&pagesize=<pagesize>')
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


@app.route('/HelloSTU/add_usr_message/', methods=['GET', 'POST'])
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
@app.route('/HelloSTU/usr_message_comment/id=<t_id>')
@cache.cached(timeout=300, key_prefix='usr_message_comment')
def usr_message_comment(t_id):
    temp = UsrMessageComment.query.filter_by(message_id=t_id, state=1).all()
    title = [i for i in range(len(temp))]

    return json.dumps(add_element2(temp, title), ensure_ascii=False)


@app.route('/HelloSTU/add_usr_message_comment/', methods=['GET', 'POST'])
def add_usr_message_comment():
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


# 7.二手交易
# 物品分类--返回：json列表
# '{"0": {"id": 1, "name": "生活用品"},
#   "1": {"id": 2, "name": "学习用品"},
#   "2": {"id": 3, "name": "饮食用品"},
#   "3": {"id": 4, "name": "娱乐用品"}}'
@app.route('/HelloSTU/goods_class/')
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
@app.route('/HelloSTU/goods_list/page=<page>&pagesize=<pagesize>')
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
@app.route('/HelloSTU/goods/id=<t_id>')
@cache.cached(timeout=300, key_prefix='goods')
def goods(t_id):
    temp = Goods.query.filter_by(id=t_id).first()

    return json.dumps(eval(str(temp)), ensure_ascii=False)


# 上传新商品
@app.route('/HelloSTU/add_goods/', methods=['GET', 'POST'])
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
@app.route('/HelloSTU/goods_comment/id=<t_id>')
@cache.cached(timeout=300, key_prefix='goods_comment')
def goods_comment(t_id):
    temp = GoodsComment.query.filter_by(goods_id=t_id, state=1).all()
    title = [i for i in range(len(temp))]

    return json.dumps(add_element2(temp, title), ensure_ascii=False)


@app.route('/HelloSTU/add_goods_comment/', methods=['GET', 'POST'])
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


# 8.我的
# 用户注册
@app.route('/HelloSTU/usr_register/', methods=['GET', 'POST'])
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
@app.route('/HelloSTU/usr_login/', methods=['GET', 'POST'])
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


# 问题分类--返回：json列表
# '{"0": {"id": 1, "name": "功能问题"},
#   "1": {"id": 2, "name": "内容问题"}}'
@app.route('/HelloSTU/question_class/')
@cache.cached(timeout=300, key_prefix='question_class')
def question_class():
    temp = QuestionC.query.all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 问题内容--返回：json列表
# '{"0": {"id": 1, "name": "地图导航问题", "content": "爱看不看", "questionC_id": 1}}'
@app.route('/HelloSTU/question/id=<t_id>')
@cache.cached(timeout=300, key_prefix='question')
def question(t_id):
    temp = Question.query.filter_by(questionC_id=t_id).all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 使用帮助分类--返回：json列表
# '{"0": {"id": 1, "name": "功能使用"}, "1": {"id": 2, "name": "内容使用"}}'
@app.route('/HelloSTU/use_class/')
@cache.cached(timeout=300, key_prefix='use_class')
def use_class():
    temp = UseC.query.all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# 帮助内容
# '{"0": {"id": 1, "name": "景点", "content": "首页点一下", "useC_id": 1}}'
@app.route('/HelloSTU/use/id=<t_id>')
@cache.cached(timeout=300, key_prefix='use')
def use(t_id):
    temp = Use.query.filter_by(useC_id=t_id).all()
    title = [i for i in range(len(temp))]

    return json.dumps(to_dict(sorted(temp, key=attrgetter('id')), title), ensure_ascii=False)


# ##################################################### 程序运行 ###################################################### #
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)