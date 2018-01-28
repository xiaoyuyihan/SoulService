from . import api
from flask import request
from app import db
from app.models import ColumnContent, UserInformation, Column, ChildColumn
import json
from .information import sendData, getCurrentDateTime

"""
搜索
"""


@api.route('/search', methods=['POST', 'GET'])
def Search():
    searchName = request.values.get('name', default="", type=str)
    data = []
    ColumnContents = ColumnContent.query.filter(
        ColumnContent.name.like("%" + searchName + "%") is not None
        or ColumnContent.subtitle.like("%" + searchName + "%")).all()
    for Column in ColumnContents:
        data.append(Column.column_dict())
    return json.dumps(sendData(True, data, 'OK'))


"""
最新
"""


@api.route('/newContent', methods=['POST', 'GET'])
def NewContent():
    page = request.values.get('page', default=1, type=int)
    ColumnContents = ColumnContent.query.order_by(ColumnContent.time.desc()) \
        .paginate(page=page, per_page=25, error_out=False)
    data = []
    for Column in ColumnContents.items:
        data.append(Column.column_dict())
    return json.dumps(sendData(True, data, 'OK'))


"""
最热
"""


@api.route('/hotContent', methods=['POST', 'GET'])
def HotContent():
    page = request.values.get('page', default=1, type=int)
    ColumnContents = ColumnContent.query.order_by(ColumnContent.live.desc()) \
        .paginate(page=page, per_page=25, error_out=False)
    data = []
    for Column in ColumnContents.items:
        data.append(Column.column_dict())
    return json.dumps(sendData(True, data, 'OK'))


"""
推荐
"""


@api.route('/recommended', methods=['POST', 'GET'])
def Recommended():
    user = request.values.get('user', default=None, type=str)
    page = request.values.get('page', default=1, type=int)
    interest = tuple(UserInformation.query.filter_by(phone=user).first().interest.split(','))

    ColumnContents = ColumnContent.query.order_by(ColumnContent.time.desc()).filter(
        ColumnContent.father_id.in_(interest)) \
        .paginate(page=page, per_page=25, error_out=False)
    data = []
    for Column in ColumnContents.items:
        data.append(Column.column_dict())
    return json.dumps(sendData(True, data, "OK"))


"""
获取内容？？？？
"""


@api.route('/obtainContent', methods=['POST', 'GET'])
def obtainContent():
    cType = request.values.get('type', default=0, type=int)
    page = request.values.get('page', default=1, type=int)
    contents = ColumnContent.query.order_by(ColumnContent.time.desc()).filter(ColumnContent.type == cType) \
        .paginate(page=page, per_page=25, error_out=False)
    data = []
    for Column in contents.items:
        data.append(Column.column_dict())
    return json.dumps(sendData(True, data, "OK"))


static_column_type_learn = 0
static_column_type_create = 1

"""
获取栏目
"""


@api.route('/obtainColumn', methods=['POST', 'GET'])
def obtainColumn():
    user = request.values.get('user', type=str)
    type = request.values.get('type', type=int)
    if type is static_column_type_learn and user is not None:
        data = obtainLearnColumn(user)
        return json.dumps(sendData(True, data, "OK"))
    elif type is static_column_type_create and user is not None:
        data = obtainCreateColumn(user)
        return json.dumps(sendData(True, data, "OK"))
    else:
        data = "参数错误"
        return json.dumps(sendData(False, data, "NOT"))


"""
获取学习栏目
"""


def obtainLearnColumn(user):
    contents = Column.query.filter(Column.accounts == user) \
        .order_by(Column.time.desc()).all()
    data = []
    for Column in contents:
        data.append(Column.column_dict())
    return data


"""
获取创造栏目
"""


def obtainCreateColumn(user):
    data = []
    return data


"""
添加栏目
"""


@api.route('/addColumn', methods=['POST', 'GET'])
def addColumn():
    user = request.values.get('user', type=str)
    type = request.values.get('type', type=int)
    name = request.values.get('name', type=str)
    introduction = request.values.get('introduction', type=str)
    time = getCurrentDateTime()
    identity = request.values.get('identity')
    if type is static_column_type_learn:
        fatherColumn = Column(accounts=user, name=name,
                                                    introduction=introduction, time=time, father_identity=identity)
        db.session.add(fatherColumn)
        db.session.commit()
        return json.dumps(sendData(True, "创建成功", "OK"))
    elif type is static_column_type_create:
        return json.dumps(sendData(True, "创建成功", "OK"))


"""
添加子栏目
"""


@api.route('/addChildColumn', methods=['POST'])
def addChildColumn():
    user = request.values.get('user', type=str)
    type = request.values.get('type', type=int)
    name = request.values.get('name', type=str)
    introduction = request.values.get('introduction', type=str)
    time = getCurrentDateTime()
    identity = request.values.get('identity')
    if type is static_column_type_learn:
        fatherColumn = ChildColumn(accounts=user, name=name,
                                            introduction=introduction, time=time, father_id=identity)
        db.session.add(fatherColumn)
        db.session.commit()
        return json.dumps(sendData(True, "创建成功", "OK"))
    elif type is static_column_type_create:
        return json.dumps(sendData(True, "创建成功", "OK"))

"""
添加学习内容
"""


@api.route('/addLearnContent', methods=['POST'])
def addLearnContent():
    name = request.values.get('name', type=str)
    subtitle = request.values.get('subtitle', type=str, default=None)
    content = request.values.get('content', type=str)
    time = getCurrentDateTime()
    accounts = request.values.get('user', type=str)
    photo = request.values.get('photo', type=str)
    video = request.values.get('video', type=str)
    audio = request.values.get('audio', type=str)
    visition = request.values.get('visition', type=int, default=0)
    type = request.values.get('type',type=int)
    richtext=request.values.get('richText',type=str)
    father_id=request.values.get('father_id',type=int)
