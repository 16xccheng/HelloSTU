# #####################################################################################################################
# 名称：HelloSTU后端数据库初始化文件--测试专用
# 作者：程晓聪
# 版本：1.0
# 修改：2019.2.2
# #####################################################################################################################


# -*- coding:utf-8 -*-
from app import *

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    # 用户基本信息
    UI1 = UsrInfo(name='学生会主席', account='16zhliu', password='16zhliu', permission='admin')
    UI2 = UsrInfo(name='网球社主席', account='16jhchen', password='16jhchen', permission='admin')
    UI3 = UsrInfo(name='青协主席', account='16xccheng', password='16xccheng', permission='admin')
    UI4 = UsrInfo(name='宋兵甲', account='16sbjia', password='16sbjia', permission='user')
    UI5 = UsrInfo(name='炮灰乙', account='16phyi', password='16phyi', permission='user')
    UI6 = UsrInfo(name='土匪丙', account='16tfbing', password='16tfbing', permission='user')
    db.session.add_all([UI1, UI2, UI3, UI4, UI5, UI6])
    db.session.commit()
    # 1.景点（无关用户）
    senery1 = Scenery(name='a', content='a', origin='a')
    senery2 = Scenery(name='b', content='b', origin='b')
    senery3 = Scenery(name='c', content='c', origin='c')
    senery4 = Scenery(name='d', content='d', origin='d')
    senery5 = Scenery(name='e', content='e', origin='e')
    db.session.add_all([senery1, senery2, senery3, senery4, senery5])
    db.session.commit()

    # 2.地图导航（无关用户）
    # 地点分类
    PlaceC1 = PlaceC(name='书院')
    PlaceC2 = PlaceC(name='上课')
    PlaceC3 = PlaceC(name='活动')
    PlaceC4 = PlaceC(name='餐饮')
    PlaceC5 = PlaceC(name='学院')
    PlaceC6 = PlaceC(name='办公')
    PlaceC7 = PlaceC(name='生活')
    PlaceC8 = PlaceC(name='其他')
    db.session.add_all([PlaceC1, PlaceC2, PlaceC3, PlaceC4, PlaceC5, PlaceC6, PlaceC7, PlaceC8])
    db.session.commit()
    # 地点
    place1 = Place(name='至诚书院', coordinate='1;1', placeC_id=PlaceC1.id)
    place2 = Place(name='E教学楼', coordinate='2;2', placeC_id=PlaceC2.id)
    place3 = Place(name='新体育馆', coordinate='3;3', placeC_id=PlaceC3.id)
    place4 = Place(name='第三食堂', coordinate='4;4', placeC_id=PlaceC4.id)
    place5 = Place(name='法学院', coordinate='5;5', placeC_id=PlaceC5.id)
    place6 = Place(name='新行政楼', coordinate='6;6', placeC_id=PlaceC6.id)
    place7 = Place(name='东门', coordinate='7;7', placeC_id=PlaceC7.id)
    place8 = Place(name='卫生间', coordinate='8;8', placeC_id=PlaceC8.id)
    place9 = Place(name='弘毅书院', coordinate='9;9', placeC_id=PlaceC1.id)
    db.session.add_all([place1, place2, place3, place4, place5, place6, place7, place8, place9])
    db.session.commit()

    # 3.学校组织信息
    # 组织分类（无关用户）
    OC1 = OrganizationC(name='组织')
    OC2 = OrganizationC(name='社团')
    db.session.add_all([OC1, OC2])
    db.session.commit()
    # 组织基本信息（无关用户）
    OI1 = OrganizationInfo(name='学生会', content='学生会', origin='学生会', organizationC_id=OC1.id)
    OI2 = OrganizationInfo(name='网球社', content='网球社', origin='网球社', organizationC_id=OC2.id)
    OI3 = OrganizationInfo(name='青协', content='青协', origin='青协', organizationC_id=OC1.id)
    db.session.add_all([OI1, OI2, OI3])
    db.session.commit()
    # 组织发布的信息
    OM1 = OrganizationMessage(title='学生会活动1', createTime=local_time(), activeTime='2018-2019',
                              state=1, content='学生会活动1', agreeNum=1, commentNum=1, writer_id=UI1.id)
    OM2 = OrganizationMessage(title='网球社活动1', createTime=local_time(), activeTime='2018-2019',
                              state=1, content='网球社活动1', agreeNum=1, commentNum=1, writer_id=UI2.id)
    OM3 = OrganizationMessage(title='青协活动1', createTime=local_time(), activeTime='2018-2019',
                              state=1, content='青协活动1', agreeNum=1, commentNum=1, writer_id=UI3.id)
    db.session.add_all([OM1, OM2, OM3])
    db.session.commit()
    # 组织发布信息评论
    OMC1 = OrganizationMessageComment(state=1, createTime=local_time(), content='我觉得学生会说得对',
                                      message_id=OM1.id, writer_id=UI4.id, replied_id=-1)
    OMC2 = OrganizationMessageComment(state=1, createTime=local_time(), content='我觉得网球社说得对',
                                      message_id=OM2.id, writer_id=UI5.id, replied_id=-1)
    OMC3 = OrganizationMessageComment(state=1, createTime=local_time(), content='我觉得青协说得对',
                                      message_id=OM3.id, writer_id=UI6.id, replied_id=-1)
    db.session.add_all([OMC1, OMC2, OMC3])
    db.session.commit()

    # 4.学校其他信息（无关用户）
    Message1 = Message(name='校训1', content='有志')
    Message2 = Message(name='校训2', content='有识')
    Message3 = Message(name='校训3', content='有恒')
    db.session.add_all([Message1, Message2, Message3])
    db.session.commit()

    # 5.学校周边（无关用户）
    # 周边分类
    PlayC1 = PlayC(name='美食')
    PlayC2 = PlayC(name='娱乐')
    PlayC3 = PlayC(name='游玩')
    PlayC4 = PlayC(name='出行')
    db.session.add_all([PlayC1, PlayC2, PlayC3, PlayC4])
    db.session.commit()
    # 周边
    play1 = Play(name='草莓冰', content='草莓冰好吃', local='十二中', phone='10086', origin='草莓冰', playC_id=PlayC1.id)
    play2 = Play(name='天天乐', content='天天乐好吃', local='鮀浦', phone='10086', origin='天天乐', playC_id=PlayC2.id)
    play3 = Play(name='小公园', content='小公园好吃', local='西堤', phone='10086', origin='小公园', playC_id=PlayC3.id)
    play4 = Play(name='潮汕站', content='潮汕站好吃', local='潮州', phone='10086', origin='潮汕站', playC_id=PlayC4.id)
    db.session.add_all([play1, play2, play3, play4])
    db.session.commit()

    # 6.社交圈子
    # 用户发布信息
    UM1 = UsrMessage(createTime=local_time(), content='我说1', agreeNum=1, commentNum=1,
                     state=1, writer_id=UI1.id)
    UM2 = UsrMessage(createTime=local_time(), content='我说2', agreeNum=2, commentNum=1,
                     state=1, writer_id=UI2.id)
    UM3 = UsrMessage(createTime=local_time(), content='我说3', agreeNum=3, commentNum=1,
                     state=1, writer_id=UI3.id)
    db.session.add_all([UM1, UM2, UM3])
    db.session.commit()
    # 用户发布信息评论
    UMC1 = UsrMessageComment(createTime=local_time(), content='我说1说得对', state=1,
                             message_id=UM1.id, writer_id=UI4.id, replied_id=-1)
    UMC2 = UsrMessageComment(createTime=local_time(), content='我说2说得对', state=1,
                             message_id=UM2.id, writer_id=UI5.id, replied_id=-1)
    UMC3 = UsrMessageComment(createTime=local_time(), content='我说3说得对', state=1,
                             message_id=UM3.id, writer_id=UI6.id, replied_id=-1)
    db.session.add_all([UMC1, UMC2, UMC3])
    db.session.commit()

    # 7.二手交易
    # 物品分类
    GC1 = GoodsC(name='生活用品')
    GC2 = GoodsC(name='学习用品')
    GC3 = GoodsC(name='饮食用品')
    GC4 = GoodsC(name='娱乐用品')
    db.session.add_all([GC1, GC2, GC3, GC4])
    db.session.commit()
    # 物品
    goods1 = Goods(name='音响', createTime=local_time(), state=1, price=999, content='音响',
                   phone='10086', commentNum=1, type='生活用品', writer_id=UI1.id)
    goods2 = Goods(name='高数', createTime=local_time(), state=1, price=999, content='高数',
                   phone='10086', commentNum=1, type='学习用品', writer_id=UI2.id)
    goods3 = Goods(name='筷子', createTime=local_time(), state=1, price=999, content='筷子',
                   phone='10086', commentNum=1, type='饮食用品', writer_id=UI3.id)
    goods4 = Goods(name='手柄', createTime=local_time(), state=1, price=999, content='手柄',
                   phone='10086', commentNum=1, type='娱乐用品', writer_id=UI4.id)
    db.session.add_all([goods1, goods2, goods3, goods4])
    db.session.commit()
    # 物品评论
    GComment1 = GoodsComment(state=1, createTime=local_time(), content='我觉得这是1手的',
                             goods_id=goods1.id, writer_id=UI2.id, replied_id=-1)
    GComment2 = GoodsComment(state=1, createTime=local_time(), content='我觉得这是2手的',
                             goods_id=goods2.id, writer_id=UI3.id, replied_id=-1)
    GComment3 = GoodsComment(state=1, createTime=local_time(), content='我觉得这是3手的',
                             goods_id=goods3.id, writer_id=UI4.id, replied_id=-1)
    GComment4 = GoodsComment(state=1, createTime=local_time(), content='我觉得这是4手的',
                             goods_id=goods4.id, writer_id=UI5.id, replied_id=-1)
    db.session.add_all([GComment1, GComment2, GComment3, GComment4])
    db.session.commit()

    # 8.我的
    # 问题分类（无关用户）
    QC1 = QuestionC(name='功能问题')
    QC2 = QuestionC(name='内容问题')
    db.session.add_all([QC1, OC2])
    db.session.commit()
    # 问题（无关用户）
    question1 = Question(name='地图导航问题', content='爱看不看', questionC_id=QC1.id)
    question2 = Question(name='制作人脱单问题', content='有一个没有', questionC_id=QC2.id)
    db.session.add_all([question1, question2])
    db.session.commit()
    # 使用帮助分类（无关用户）
    UC1 = UseC(name='功能使用')
    UC2 = UseC(name='内容使用')
    db.session.add_all([UC1, UC2])
    db.session.commit()
    # 使用帮助（无关用户）
    use1 = Use(name='景点', content='首页点一下', useC_id=UC1.id)
    use2 = Use(name='周边', content='点进去', useC_id=UC2.id)
    db.session.add_all([use1, use2])
    db.session.commit()