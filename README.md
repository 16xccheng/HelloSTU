# 服务器接口文档

## 统一接口前缀：

http://120.77.36.131/HelloSTU



## API（注：静态为与用户无关，动态为与用户有关）

## 一.景点

### 1.景点（静态）

#### 请求URL

前缀+/scenery_info/name=<t_name>

#### 请求方式

GET

#### 请求参数

URL中的   t_name，即对应景点名字

#### 返回例子

```
{
 	'id':6,
 	'name':'2019.2.16',
 	'content':'2019.2.16',
 	'image':'http://120.77.36.131/_uploads/images/88x7uv4draw6qs22.png',
 	'origin':'2019.2.16'
 }
```

#### 返回参数说明

| 参数名  | 类型   | 说明         |
| ------- | ------ | ------------ |
| id      | int    | 景点id       |
| name    | string | 景点名称     |
| content | string | 景点说明     |
| image   | string | 景点图片url  |
| origin  | string | 景点信息来源 |

#### 备注：

（测试）可上传新景点http://120.77.36.131/HelloSTU/add_scenery/



## 二.地图导航

### 2.1地点分类（静态）

#### 请求URL

前缀+/place_class/

#### 请求方式

GET

#### 请求参数

无

#### 返回例子

```
{
	"0": {
		"id": 1, 
		"name": "书院"
		},
    "1": {
    	"id": 2, 
    	"name": "上课"
    	},
    "2": {
    	"id": 3, 
    	"name": "活动"
    	},
    "3": {
    	"id": 4, 
    	"name": "餐饮
    	},
    "4": {
    	"id": 5, 
    	"name": "学院"
    	},
    "5": {
     	"id": 6, 
     	"name": "办公"
     	},
    "6": {
    	"id": 7, 
    	"name": "生活"
    	},
    "7": {
    	"id": 8, 
    	"name": "其他"
    	}
}
```

#### 返回参数说明

| 参数名 | 类型   | 说明     |
| ------ | ------ | -------- |
| id     | int    | 类别id   |
| name   | string | 类别名称 |



### 2.2地点具体内容

#### 请求URL

前缀+/place_list/id=<t_id>

#### 请求方式

GET

#### 请求参数

URL中的 t_id，即对应地点id

#### 返回例子

```
{
	"0": {
		"id": 1, 
		"name": "至诚书院", 
		"coordinate": "1;1", 
		"placeC_id": 1
		},
  	"1": {
  		"id": 9, 
  		"name": "弘毅书院", 
  		"coordinate": "9;9", 
  		"placeC_id": 1
  		}
}
```

#### 返回参数说明

| 参数名     | 类型   | 说明           |
| ---------- | ------ | -------------- |
| id         | int    | 地点id         |
| name       | string | 地点名称       |
| coordinate | string | 地点坐标       |
| placeC_id  | int    | 地点所属类别id |

#### 备注

coordinate内容有  ;  隔开，经度;纬度

（测试）可上传新地点http://120.77.36.131//HelloSTU/add_place/



## 三.学校组织信息

### 3.1学校组织列表（静态）

#### 请求URL

前缀+/organization_class/

#### 请求方式

GET

#### 请求参数

无

#### 返回例子

```
{
   "社团": {
   			"0": {"id": 2, "name": "网球社"}
   		  },
   "组织": {
   			"0": {"id": 1, "name": "学生会"},
           	 "1": {"id": 3, "name": "青协"}
           }
}
```

#### 返回参数说明

| 参数名 | 类型   | 说明         |
| ------ | ------ | ------------ |
| id     | int    | 对应组织id   |
| name   | string | 对应组织名称 |

#### 备注

返回例子前的“社团”和“组织”为分类类别



### 3.2组织基本信息（静态）

#### 请求URL

前缀+/organization_info/name=<t_name>

#### 请求方式

GET

#### 请求参数

url中的 t_name，即对应组织名称

#### 返回例子

```
{
	"id": 1, 
	"name": "学生会", 
	"content": "学生会", 
	"image": "None", 
	"origin": "学生会", 
	"organizationC_id": "1"
}
```

#### 返回参数说明

| 参数名           | 类型   | 说明            |
| ---------------- | ------ | --------------- |
| id               | int    | 组织id          |
| name             | string | 组织名称        |
| content          | string | 组织介绍        |
| image            | stirng | 组织图片对应url |
| origin           | string | 组织信息来源    |
| organizationC_id | int    | 组织所属类别id  |

#### 备注：

（测试）可上传新组织http://120.77.36.131/HelloSTU/add_organization/



### 3.3组织发布信息列表（动态）

#### 请求URL

前缀+/organization_message/page=<page>&pagesize=<pagesize>

#### 请求方式

GET

#### 请求参数

url中的“page”和“pagesize”，即请求页码和请求页面大小

#### 返回例子

```
{
	"0": {
		"id": 1, 
		"title": "学生会活动1", 
		"createTime": "2019-02-10 17:03:36", 
		"activeTime": "2018-2019", 
		"state": 1, 
		"content": "学生会活动1", 
		"image": "None", 
		"agreeNum": 1, 
		"attachment": "None", 
		"commentNum": 10, 
		"writer_id": 1, 
		"writer_name": "学生会主席"
		},
  	"1": {
  		"id": 2, 
  		"title": "网球社活动1", 
  		"createTime": "2019-02-10 17:03:36", 
  		"activeTime": "2018-2019", 
  		"state": 1, 
  		"content": "网球社活动1", 
  		"image": "None", 
  		"agreeNum": 1, 
  		"attachment": "None", 
  		"commentNum": 1, 
  		"writer_id": 2, 
  		"writer_name": "网球社主席"
  		},
  	"2": {
  		"id": 3, 
  		"title": "青协活动1", 
  		"createTime": "2019-02-10 17:03:36", 
  		"activeTime": "2018-2019", 
  		"state": 1, 
  		"content": "青协活动1", 
  		"image": "None", 
  		"agreeNum": 1, 
  		"attachment": "None", 
  		"commentNum": 1, 
  		"writer_id": 3, 
  		"writer_name": "青协主席"
  		}
}
```

#### 返回参数说明

| 参数名      | 类型   | 说明        |
| ----------- | ------ | ----------- |
| id          | int    | 信息id      |
| title       | string | 信息标题    |
| createTime  | string | 创建时间    |
| activeTime  | string | 活动时间    |
| state       | int    | 状态        |
| content     | string | 信息内容    |
| image       | string | 附加图片url |
| agreeNum    | int    | 点赞数      |
| attachment  | string | 附件url     |
| commentNum  | int    | 评论数      |
| writer_id   | int    | 作者id      |
| writer_name | string | 作者名称    |

#### 备注

状态：1为有效，0为无效



### 3.4组织发布信息（动态）

#### 请求URL

前缀+/add_organization_message/

#### 请求方式

POST

#### 请求参数

| 参数名     | 必要性 | 类型   | 说明         |
| ---------- | ------ | ------ | ------------ |
| writer_id  | 是     | int    | 作者id       |
| token      | 是     | string | 验证签名     |
| title      | 否     | string | 信息名称     |
| activeTime | 否     | string | 信息活动时间 |
| content    | 是     | string | 信息内容     |
| images     | 否     | string | 信息图片url  |
| attachment | 否     | string | 信息附件链接 |

#### 返回例子

| 返回内容 |
| :------: |
| 上传成功 |
| 添加失败 |
| 参数出错 |
| 登陆超时 |

#### 备注

token保存在客户端



### 3.5对应组织发布信息评论（动态）

#### 请求URL

前缀+/organization_message_comment/id=<t_id>

#### 请求方式

GET

#### 请求参数

url中的 t_id， 即对应的组织信息id

#### 返回例子

```
{
	"0": {
			"id": 1, 
			"state": 1, 
			"createTime": "2019-02-10 17:03:36", 
			"content": "我觉得学生会说得对", 
			"writer_id": 4, 
			"replied_id": -1, 
			"message_id": 1, 
			"writer_name": "宋兵甲", 
			"replied_name": "null"
	  	}
}
```

#### 返回参数说明

| 参数名       | 类型   | 说明           |
| ------------ | ------ | -------------- |
| id           | int    | 评论id         |
| state        | int    | 评论状态       |
| createTime   | string | 评论创建时间   |
| content      | string | 评论内容       |
| writer_id    | int    | 发布者id       |
| replied_id   | int    | 被回复者id     |
| message_id   | int    | 对应评论信息id |
| writer_name  | string | 发布者名称     |
| replied_name | string | 被回复者名称   |

#### 备注

replied_id若为-1，则无被回复者，replied_name返回值为null



### 3.6用户发布组织信息评论（动态）

#### 请求URL

前缀+/add_organization_message_comment/

#### 请求方式

POST

#### 请求参数

| 参数名     | 必要性 | 类型   | 说明       |
| ---------- | ------ | ------ | ---------- |
| writer_id  | 是     | int    | 作者id     |
| token      | 是     | string | 验证签名   |
| content    | 是     | string | 评论内容   |
| replied_id | 是     | int    | 被回复者id |
| message_id | 是     | int    | 回复信息id |

#### 返回例子

| 返回内容 |
| :------: |
| 上传成功 |
| 添加失败 |
| 参数出错 |
| 登陆超时 |

#### 备注

token保存在客户端，无被回复者则传输replied_id为-1



## 四.学校其他信息

### 4.1学校其他信息（静态）

#### 请求URL

前缀+/message_list/

#### 请求方式

GET

#### 请求参数

无

#### 返回例子

```
{
		"1": "校训1",
    	"2": "校训2",
    	"3": "校训3"
}
```

#### 返回参数说明

前面编号为id， 后面字符串为信息名称



### 4.2具体信息（静态）

#### 请求URL

前缀+/message_info/name=<t_name>

#### 请求方式

GET

#### 请求参数

url中的 t_name，即对应信息的名称

#### 返回例子

```
{
	"id": 1, 
	"name": "校训1", 
	"content": "有志", 
	"image": "None"
}
```

#### 返回参数说明

| 参数名  | 类型   | 说明        |
| ------- | ------ | ----------- |
| id      | int    | 信息id      |
| name    | string | 信息名称    |
| content | string | 信息内容    |
| image   | string | 信息图片url |



## 五.学校周边

### 5.1学校周边类别（静态）

#### 请求URL

前缀+/play_class/

#### 请求方式

GET

#### 请求参数

无

#### 返回例子

```
{"0": {"id": 1, "name": "美食"},
#   "1": {"id": 2, "name": "娱乐"},
#   "2": {"id": 3, "name": "游玩"},
#   "3": {"id": 4, "name": "出行"}}
```

#### 返回参数说明

| 参数名 | 类型 | 说明         |
| ------ | ---- | ------------ |
| id     | int  | 周边类别id   |
| name   | str  | 周边类别名称 |

#### 备注

（测试）可上传新周边http://120.77.36.131/HelloSTU/add_play/



### 5.2周边列表（静态）

#### 请求URL

前缀+/play_list/class_id=<t_class_id>

#### 请求方式

GET

#### 请求参数

url中的 t_class_id，即对应周边类别id

#### 返回例子

```
{
	"0": {
		"id": 1, 
		"name": "草莓冰", 
		"content": "草莓冰好吃", 
		"image": null
		}
}
```

#### 返回参数说明

| 参数名  | 类型   | 说明       |
| ------- | ------ | ---------- |
| id      | int    | 对应周边id |
| name    | string | 周边名称   |
| content | string | 周边简介   |
| image   | string | 周边图片   |

#### 备注

返回内容为一个列表，包含多个周边信息



### 5.3周边具体信息（静态）

#### 请求URL

前缀+/play/id=<t_id>

#### 请求方式

GET

#### 请求参数

url中的 t_id，即对应信息id

#### 返回例子

```
{
	"id": 1, 
	"name": "草莓冰", 
	"content": "草莓冰好吃", 
	"image": "None", 
	"local": "十二中", 
	"phone": "10086", 
	"origin": "草莓冰", 
	"playC_id": 1
}
```

#### 返回参数说明

| 参数名   | 类型   | 说明           |
| -------- | ------ | -------------- |
| id       | int    | 周边id         |
| name     | string | 周边名称       |
| content  | string | 周边内容       |
| image    | string | 周边图片url    |
| local    | string | 周边地址       |
| phone    | string | 周边对应电话   |
| origin   | string | 周边信息来源   |
| playC_id | int    | 周边所属类别id |



## 六.社交圈子

### 6.1用户发布信息列表（动态）

#### 请求URL

前缀+/usr_message/page=<page>&pagesize=<pagesize>

#### 请求方式

GET

#### 请求参数

url中的“page”和“pagesize”，即页码和页面大小

#### 返回例子

```
{
	"0": {
		"id": 1, 
		"createTime": "2019-02-10 17:03:36", 
		"content": "我说1", 
		"image": "None", 
		"agreeNum": 1, 
		"commentNum": 1, 
		"state": 1, 
		"writer_id": 1, 
		"writer_name": "学生会主席"
		},
  	"1": {
  		"id": 2, 
  		"createTime": "2019-02-10 17:03:36", 
  		"content": "我说2", 
  		"image": "None", 
  		"agreeNum": 2, 
  		"commentNum": 1, 
  		"state": 1, 
  		"writer_id": 2, 
  		"writer_name": "网球社主席"
  		},
  	"2": {
  		"id": 3, 
  		"createTime": "2019-02-10 17:03:36", 
  		"content": "我说3", 
  		"image": "None", 
  		"agreeNum": 3, 
  		"commentNum": 1, 
  		"state": 1, 
  		"writer_id": 3, 
  		"writer_name": "青协主席"
  		}
}
```

#### 返回参数说明

| 参数名      | 类型   | 说明            |
| ----------- | ------ | --------------- |
| id          | int    | 信息id          |
| createTime  | string | 信息创建时间    |
| content     | string | 信息内容        |
| image       | string | 信息包含图片url |
| agreeNum    | int    | 点赞数          |
| commentNum  | int    | 评论数          |
| state       | int    | 信息状态        |
| writer_id   | int    | 发布者id        |
| writer_name | string | 发布者名称      |



### 6.2用户发布信息（动态）

#### 请求URL

前缀+/add_usr_message/

#### 请求方式

POST

#### 请求参数

| 参数名    | 必要性 | 类型   | 说明        |
| --------- | ------ | ------ | ----------- |
| writer_id | 是     | int    | 作者id      |
| token     | 是     | string | 验证签名    |
| content   | 是     | string | 信息内容    |
| images    | 否     | string | 信息图片url |

#### 返回例子

| 返回内容 |
| :------: |
| 上传成功 |
| 添加失败 |
| 参数出错 |
| 登陆超时 |

#### 备注

token保存在客户端



### 6.3用户信息评论（动态）

#### 请求URL

前缀+/usr_message_comment/id=<t_id>

#### 请求方式

GET

#### 请求参数

url中的 t_id，即对应信息id

#### 返回例子

```
{
	"0": {
		"id": 1, 
		"createTime": "2019-02-10 17:03:36", 
		"content": "我说1说得对", 
		"state": 1, 
		"writer_id": 4, 
		"replied_id": -1, 
		"message_id": 1, 
		"writer_name": "宋兵甲", 
		"replied_name": "null"
		}
}
```

#### 返回参数说明

| 参数名       | 类型   | 说明         |
| ------------ | ------ | ------------ |
| id           | int    | 评论id       |
| createTime   | string | 评论发布时间 |
| content      | string | 评论内容     |
| state        | int    | 评论状态     |
| writer_id    | int    | 发布者id     |
| replied_id   | int    | 被回复者id   |
| message_id   | int    | 信息id       |
| writer_name  | string | 发布者名称   |
| replied_name | string | 被回复者名称 |



### 6.4用户发布信息评论（动态）

#### 请求URL

前缀+/add_usr_message_comment/

#### 请求方式

POST

#### 请求参数

| 参数名     | 必要性 | 类型   | 说明       |
| ---------- | ------ | ------ | ---------- |
| writer_id  | 是     | int    | 作者id     |
| token      | 是     | string | 验证签名   |
| content    | 是     | string | 信息内容   |
| replied_id | 是     | int    | 被回复者id |
| message_id | 是     | int    | 回复信息id |

#### 返回例子

| 返回内容 |
| :------: |
| 上传成功 |
| 添加失败 |
| 参数出错 |
| 登陆超时 |

#### 备注

token保存在客户端，无被回复者则传输replied_id为-1



## 七.二手交易

### 7.1物品分类（动态）

#### 请求URL

前缀+/goods_class/

#### 请求方式

GET

#### 请求参数

无

#### 返回例子

```
{"0": {"id": 1, "name": "生活用品"},
#   "1": {"id": 2, "name": "学习用品"},
#   "2": {"id": 3, "name": "饮食用品"},
#   "3": {"id": 4, "name": "娱乐用品"}}
```

#### 返回参数说明

| 参数名 | 类型   | 说明     |
| ------ | ------ | -------- |
| id     | int    | 类别id   |
| name   | string | 类别名称 |



### 7.2物品列表（动态）

#### 请求URL

前缀+/goods_list/page=<page>&pagesize=<pagesize>

#### 请求方式

GET

#### 请求参数

url中的“page”和“pagesize”，即页码和页数

#### 返回例子

```
{
	"0": {
		"id": 1, 
		"name": "音响", 
		"createTime": "2018-1-31 13:31:13", 
		"image": null
		},
   	"1": {
   		"id": 2, 
   		"name": "高数", 
   		"createTime": "2018-1-31 13:31:13", 
   		"image": null
   		},
   	"2": {
   		"id": 3, 
   		"name": "筷子", 
   		"createTime": "2018-1-31 13:31:13", 
   		"image": null
   		},
   	"3": {
   		"id": 4, 
   		"name": "手柄", 
   		"createTime": "2018-1-31 13:31:13", 
   		"image": null
   		}
}
```

#### 返回参数说明

| 参数名     | 类型   | 说明         |
| ---------- | ------ | ------------ |
| id         | int    | 物品id       |
| name       | string | 物品名称     |
| createTime | string | 物品发布时间 |
| image      | string | 物品图片     |



### 7.3物品详情（动态）

#### 请求URL

前缀+/goods/id=<t_id>

#### 请求方式

GET

#### 请求参数

url中的 t_id，即对应物品id

#### 返回例子

```
{
	"id": 1, 
	"name": "音响", 
	"createTime": "2018-1-31 13:31:13", 
	"state": 1, 
	"price": 999, 
	"content": "音响", 
	"image": "None", 
	"phone": "10086", 
	"wechat": "None", 
	"email": "None", 
	"commentNum": 1, 
	"writer_id": 1, 
	"type": "生活用品"
}
```

#### 返回参数说明

| 参数名     | 类型   | 说明         |
| ---------- | ------ | ------------ |
| id         | int    | 物品id       |
| name       | string | 物品名称     |
| createTime | string | 物品发布时间 |
| state      | int    | 物品状态     |
| price      | int    | 物品价格     |
| content    | string | 物品介绍     |
| image      | string | 物品图片url  |
| phone      | string | 发布者电话   |
| wechat     | string | 发布者微信   |
| email      | string | 发布者邮箱   |
| commentNum | int    | 评论数       |
| writer_id  | int    | 发布者id     |
| type       | string | 物品类别     |



### 7.4用户发布商品（动态）

#### 请求URL

前缀+/add_goods/

#### 请求方式

POST

#### 请求参数

| 参数名    | 必要性 | 类型   | 说明        |
| --------- | ------ | ------ | ----------- |
| writer_id | 是     | int    | 发布者id    |
| token     | 是     | string | 验证签名    |
| name      | 是     | string | 商品名称    |
| price     | 是     | int    | 商品价格    |
| content   | 是     | string | 商品简介    |
| images    | 是     | string | 商品图片url |
| phone     | 是     | string | 发布者电话  |
| wechat    | 是     | string | 发布者微信  |
| email     | 是     | string | 发布者邮箱  |
| type      | 是     | string | 商品类别    |

#### 返回例子

| 返回内容 |
| :------: |
| 上传成功 |
| 添加失败 |
| 参数出错 |
| 登陆超时 |

#### 备注

token保存在客户端



### 7.6物品评论（动态）

#### 请求URL

前缀+/goods_comment/id=<t_id>

#### 请求方式

GET

#### 请求参数

url中 t_id，即对应物品id

#### 返回例子

```
{
	"0": {
		"id": 1, 
		"state": 1, 
		"createTime": "2019-02-10 17:03:36", 
		"content": "我觉得这是1手的", 
		"writer_id": 2, 
		"replied_id": -1, 
		"goods_id": 1, 
		"writer_name": "网球社主席", 
		"replied_name": "null"
		}
}
```

#### 返回参数说明

| 参数名       | 类型   | 说明         |
| ------------ | ------ | ------------ |
| id           | int    | 评论id       |
| state        | int    | 评论状态     |
| createTime   | string | 评论发布时间 |
| content      | string | 评论内容     |
| writer_id    | int    | 发布者id     |
| replied_id   | int    | 被回复者id   |
| goods_id     | int    | 物品id       |
| writer_name  | string | 发布者名称   |
| replied_name | string | 被回复者名称 |



### 7.7用户发布商品评论（动态）

#### 请求URL

前缀+/add_usr_message_comment/

#### 请求方式

POST

#### 请求参数

| 参数名     | 必要性 | 类型   | 说明       |
| ---------- | ------ | ------ | ---------- |
| writer_id  | 是     | int    | 作者id     |
| token      | 是     | string | 验证签名   |
| content    | 是     | string | 信息内容   |
| replied_id | 是     | int    | 被回复者id |
| goods_id   | 是     | int    | 回复信息id |

#### 返回例子

| 返回内容 |
| :------: |
| 上传成功 |
| 添加失败 |
| 参数出错 |
| 登陆超时 |

#### 备注

token保存在客户端，无被回复者则传输replied_id为-1



## 八.我的

### 8.1用户注册（动态）

#### 请求URL

前缀+/usr_register/

#### 请求方式

POST

#### 请求参数

| 参数名   | 必要性 | 类型   | 说明 |
| -------- | ------ | ------ | ---- |
| name     | 是     | string | 昵称 |
| account  | 是     | string | 账号 |
| password | 是     | string | 密码 |

#### 返回例子

|  参数名  |
| :------: |
| 注册成功 |
| 注册失败 |
| 参数出错 |

#### 备注

账号account不能重复



### 8.2用户登录（动态）

#### 请求URL

前缀+/usr_login/

#### 请求方式

POST

#### 请求参数

| 参数名   | 必要性 | 类型   | 说明 |
| -------- | ------ | ------ | ---- |
| account  | 是     | string | 账号 |
| password | 是     | string | 密码 |

#### 返回例子

```
{"id": 12, "name": "cxc", "account": "16xccheng3", "permission": "user",
#  "token": "MTU1MDQxNTY3MC4zMDQ3NTQzOmQzOGQ5MGQ1YmZhMmVjNWVlMjdiYjRiMzkyMjA3MjUzMTdkYTViMWE="}
```

#### 返回参数说明

| 参数名     | 类型   | 说明     |
| ---------- | ------ | -------- |
| id         | int    | 用户id   |
| name       | string | 用户名称 |
| account    | string | 用户账号 |
| permission | string | 用户权限 |
| token      | string | 验证签名 |

#### 备注

权限分为管理者（admin）和用户（user），默认为用户（user），token要保存在本地



### 8.3问题分类（静态）

#### 请求URL

前缀+/question_class/

#### 请求方式

GET

#### 请求参数

无

#### 返回例子

```
{
	"0": {"id": 1, "name": "功能问题"},
 	"1": {"id": 2, "name": "内容问题"}
}
```

#### 返回参数说明

| 参数名 | 类型   | 说明     |
| ------ | ------ | -------- |
| id     | int    | 分类id   |
| name   | string | 分类名称 |



### 8.4问题内容（静态）

#### 请求URL

前缀+/question/id=<t_id>

#### 请求方式

GET

#### 请求参数

url中的 t_id，即对应类别id

#### 返回例子

```
{
	"0": {
		"id": 1, 
		"name": "地图导航问题", 
		"content": "爱看不看", 
		"questionC_id": 1
		}
}
```

#### 返回参数说明

| 参数名       | 类型   | 说明           |
| ------------ | ------ | -------------- |
| id           | int    | 问题id         |
| name         | string | 问题标题       |
| content      | string | 问题内容       |
| questionC_id | int    | 问题所属类别id |



### 8.5使用帮助分类（静态）

#### 请求URL

前缀+/use_class/

#### 请求方式

GET

#### 请求参数

无

#### 返回例子

```
{
	"0": {"id": 1, "name": "功能使用"}, 
	"1": {"id": 2, "name": "内容使用"}
}
```

#### 返回参数说明

| 参数名 | 类型   | 说明     |
| ------ | ------ | -------- |
| id     | int    | 类别id   |
| name   | string | 类别名称 |



### 8.6帮助内容（静态）

#### 请求URL

前缀+/use/id=<t_id>

#### 请求方式

GET

#### 请求参数

url中的 t_id，即分类id

#### 返回例子

```
{
	"0": {
		"id": 1, 
		"name": "景点", 
		"content": "首页点一下", 
		"useC_id": 1
		}
}
```

#### 返回参数说明

| 参数名  | 类型   | 说明               |
| ------- | ------ | ------------------ |
| id      | int    | 使用帮助id         |
| name    | string | 使用帮助标题       |
| content | string | 使用帮助内容       |
| useC_id | int    | 使用帮助所属类别id |

