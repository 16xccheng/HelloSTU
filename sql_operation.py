#!/usr/bin/env python 
# -*- coding:utf-8 -*-

'''
# 删除表格(别乱用)
db.drop_all()

# 声明表格
db.create_all()

# 增加
user = User(name='cxc', role_id=role.id)
db.session.add(user)
db.session.commit()

# 修改
user.name='cheng'
db.session.commit()

# 删除
db.session.delete(user)
db.session.commit()

# 添加一个角色和两个用户
# 角色
>>> role=Role(name='admin')
>>> db.session.add(role)
>>> db.session.commit()
# 用户
>>> user1=User(name='zs',role_id=role.id)
>>> user2=User(name='ls',role_id=role.id)
>>> db.session.add_all([user1,user2])
>>> db.session.commit()
>>> role.users
[<User:zs 1 None None>, <User:ls 2 None None>]
>>> user1.role
<Role:admin 1>
>>> user2.role
<Role:admin 1>

# 查看所有
>>> User.query.all()
[<User:wang 1 wang 12345>, <User:zhang 2 zhang 12345>, <User:chen 3 chen 12345>, <User:zhou 4 zhou 12345>, <User:tang 5 tang 12345>, <User:wu 6 wu 12345>, <User:qian 7 qian 12345>, <User:liu 8 liu 12345>, <User:li 9 li 12345>, <User:sun 10 sun 12345>]
# 查看数量
>>> User.query.count()
10
# 查看第一个
>>> User.query.first()
<User:wang 1 wang 12345>
# 查看第四个（3种）
>>> User.query.get(4)
<User:zhou 4 zhou 12345>
# 注意filter的‘=’和‘==’的区别
# filter功能 > filter_by功能，可以满足更多的查询条件（支持比较运算符）
>>> User.query.filter_by(id=4).first()
<User:zhou 4 zhou 12345>
>>> User.query.filter(User.id==4).first()
<User:zhou 4 zhou 12345>
>>>
'''