# 接口
import os

from . import api
from flask import request, g
from flask_login import login_user, logout_user, login_required, current_user
import random
import time, datetime
from tool import aliyun_MSM
import uuid
from app.models import ValidateCode, Major, UserInformation, \
    UserRegistered, Login, Column, ChildColumn, Description, Content, Preference, \
    Subject, Orientation
from app import db, auth, login_manager
from manage import photos, app
import json

"""
测试
"""


@api.route('/api/', methods=['GET', "POST"])
def Test():
    return "SOUL"


"""
注册接口
"""


@api.route('/api/registered', methods=['POST'])
def registered():
    file_url = ""
    phone = request.values.get('phone', default=None, type=str)  # 手机号
    try:
        user = UserInformation.query.filter_by(phone=phone).first()
    except Exception as e:
        user = None
    if user is None:
        if 'avatar' in request.files:
            for filename in request.files.getlist('avatar'):
                filename = photos.save(filename, folder='photos/avatar')
                file_url = photos.url(filename)
        else:
            file_url = os.getcwd() + '\\photos\\test.jpg'
        email = request.values.get('email', default=None, type=str)  # 邮箱
        username = request.values.get('username', default=None, type=str)  # 用户名
        password = request.values.get('password', default=None, type=str)  # 密码
        source = request.values.get('source', default=0, type=int)  # 注册来源
        registered_time = getCurrentDateTime()  # 注册时间
        user_status = request.values.get('status', default=0, type=int)  # 账户状态
        sex = request.values.get('sex', default=0, type=int)  # 性别
        birthday = StrToDate(request.values.get('birthday', default=None, type=str))  # 生日
        uuid = request.values.get('sex', default='', type=str)  # 客户端唯一ID
        introduction = request.values.get('introduction', default='请填写签名', type=str)  # 签名
        address = request.values.get('address', default=None, type=str)  # 地址
        learnInterests = InformationSplit(request.values.get('learnInterest', default=None, type=str))  # 学习兴趣点
        manufactureInterests = InformationSplit(
            request.values.get('manufactureInterest', default=None, type=str))  # 制造兴趣点

        userRegistered = UserRegistered(phone=phone, sourceint=source, registered_time=registered_time)
        userInformation = UserInformation(phone=phone, email=email, username=username, user_status=user_status,
                                          password=password, avatar=file_url, sex=sex, birthday=birthday,
                                          uuid=uuid, introduction=introduction, address=address, permissions=0)
        db.session.add(userRegistered)
        db.session.add(userInformation)
        for tp, interests in {'0': learnInterests, '1': manufactureInterests}.items():
            for interest in interests:
                preferences = Preference(phone=phone, child_column_id=int(interest), preference_type=int(tp),
                                         found_time=registered_time)
                db.session.add(preferences)

        db.session.commit()
        return json.dumps(sendData(True, "注册成功", 'OK'))
    else:
        return json.dumps(sendData(False, "该手机号已注册，如忘记密码请找回密码。", "ERROR_ACCOUNT_REGISTERED"))


def StrToDate(date):
    if date is None:
        return None
    else:
        return datetime.datetime.strptime(date, '%Y-%m-%d')


def InformationSplit(information):
    if information is None:
        informations = []
    else:
        informations = information.split(',')
    return informations


"""
登录接口
"""


@api.route('/api/login', methods=['POST', 'GET'])
def login():
    phone = request.values.get('username', default=None, type=str)
    password = request.values.get('password', default=None, type=str)
    login_time = getCurrentDateTime()
    login_ip = str(request.remote_addr)
    login_mode = request.values.get('mode', default=None, type=int)
    longitude = request.values.get('longitude', default='', type=str)
    latitude = request.values.get('latitude', default='', type=str)
    location = request.values.get('location', default='', type=str)
    login = Login(phone=phone, login_time=login_time, login_ip=login_ip, login_mode=login_mode,
                  longitude=longitude, latitude=latitude, location=location)
    try:
        user = UserInformation.query.filter_by(phone=phone).first()
    except Exception as e:
        user = None
    if user is not None and user.verify_password(password):
        login.state = 1
        data = json.dumps(sendData(True, {"token": str(user.generate_auth_token()), "msg": "登陆成功"}, 'OK'))
        login_user(user)
    elif user is None:
        login.state = 0
        data = json.dumps(sendData(False, "该帐号未注册，请注册后再次登录", 'ERROR_NO_USER'))

    else:
        login.state = -1
        data = json.dumps(sendData(False, "密码错误，请确认密码后登录", 'ERROR_PASSWORD'))

    db.session.add(login)
    db.session.commit()
    return data


"""
修改密码
"""


@api.route("/api/changePassword", methods=["POST", "GET"])
def changePassword():
    phone = request.values.get('username', default=None, type=str)
    password = request.values.get('password', default=None, type=str)
    try:
        user = UserInformation.query.filter_by(phone=phone).first();
    except Exception as e:
        user = None
    if user is None:
        return json.dumps(sendData(False, "该手机号未注册", 'ERROR_NO_USER'))
    user.password = password
    db.session.add(user)
    db.session.commit()
    return json.dumps(sendData(True, "修改完成,请登录", 'OK'))


"""
获取验证
"""


@api.route('/api/getVerification', methods=['POST', 'GET'])
def getVerification():
    phone = request.values.get('phone', default=None, type=str)  # 手机号
    verification = getVerificationCode()  # 验证码
    currentTime = time.time()  # 当前时间
    Time = getCurrentDateTime()
    while True:
        dataBytes = sendMSM(phone, verification)
        if isinstance(dataBytes, bytes):
            data = eval(dataBytes)
            message = data.get('Message')
            state = data.get('Code')
            BizId = data.get('BizId')
            RequestId = data.get('RequestId')
            validateCode = ValidateCode(phone=phone, validate=verification,
                                        time=currentTime, standard_time=Time,
                                        message=message, state=state)
            db.session.add(validateCode)
            db.session.commit()
            if message == "OK":
                person = {
                    "Flag": True,
                    "phone": phone,
                    "verification": verification,
                    "time": currentTime,
                    "state": "OK"
                }
                return json.dumps(person)
                break
            elif state == 'isv.BUSINESS_LIMIT_CONTROL':
                person = {
                    "Flag": False,
                    "phone": phone,
                    "verification": verification,
                    "time": currentTime,
                    "state": "isv.BUSINESS_LIMIT_CONTROL"
                }
                return json.dumps(person)
                break


"""
返回专业
"""


@api.route('/api/getMajor', methods=['POST', 'GET'])
def getMajor():
    fathers = Major.query.all()
    datas = []
    for father in fathers:
        data = {"name": father.name,
                "identity": father.identity,
                "introduction": father.introduction,
                "picture": father.picture,
                "child": getSubject(father.child)
                }
        datas.append(data)
    return json.dumps(sendData(True, datas, 'OK'))


"""
获取旗下专业学科
"""


def getSubject(modules):
    datas = []
    for module in modules:
        data = {"name": module.name,
                "identity": module.identity,
                "introduction": module.introduction,
                "picture": module.picture,
                "father_id": module.father_id}
        datas.append(data)
    return datas


"""
获取DIY的方向
"""


@api.route('/api/getOrientation', methods=['POST', 'GET'])
def getOrientation():
    fathers = Orientation.query.all()
    datas = []
    for father in fathers:
        data = {"name": father.name,
                "identity": father.identity,
                "introduction": father.introduction,
                "url": father.url,
                "picture": father.picture,
                "child": getDescription(father.child)
                }
        datas.append(data)
    return json.dumps(sendData(True, datas, 'OK'))


"""
方向下的种类
"""


def getDescription(modules):
    datas = []
    for module in modules:
        data = {"name": module.name,
                "identity": module.identity,
                "introduction": module.introduction,
                "picture": module.picture,
                "father_id": module.father_id}
        datas.append(data)
    return datas


"""
提交专业
@ name: 名称
@ identity: id
@ registered: 时间
@ founder： 注册人
@ introduction： 内容
@ majorType：0 设置专业 1设置科目 2 设置DIY方向 3 设置DIY类型
@ father_id ：父ID
@ picture： 附件照片
"""


@api.route('/api/setModular', methods=['POST', 'GET'])
@login_required
def setModular():
    name = request.values.get('name', type=str)
    identity = request.values.get('id', type=int)
    registered_time = getCurrentDateTime()
    founder = current_user.get_id()
    introduction = request.values.get('introduction', type=str)
    majorType = request.values.get('type', type=int)
    father_id = request.values.get('father_id', type=int)
    file_url = saveRequestFile(value='picture')

    if majorType is 0:
        column = Major(name=name, identity=identity, time=registered_time, founder=founder,
                       introduction=introduction, picture=file_url, url='')
    elif majorType is 1:
        column = Subject(name=name, identity=identity, time=registered_time, founder=founder,
                         introduction=introduction, picture=file_url, father_id=father_id, url='')
    elif majorType is 3:
        column = Description(name=name, identity=identity, time=registered_time, founder=founder,
                             introduction=introduction, picture=file_url, father_id=father_id, url='')
    elif majorType is 2:
        column = Orientation(name=name, identity=identity, time=registered_time, founder=founder,
                             introduction=introduction, picture=file_url, url='')
    db.session.add(column)
    db.session.commit()
    return json.dumps(sendData(True, "提交成功", "OK"))


"""
获取某个学科下的栏目
@fatherID      父ID    0 全部
@:columnType          类型   0 学科     1 创造      2 全部
@phone          用户
"""


@api.route("/api/getColumn", methods=['POST', 'GET'])
@login_required
def getColumn():
    columnType = request.values.get('columnType', default=2, type=int)
    fatherID = request.values.get('fatherID', default=0, type=str)
    phone = current_user.get_id()

    # 全部类型
    if columnType is 2:
        # 无父ID
        if fatherID is 0:
            columns = Column.query.filter_by(phone=phone).order_by(Column.time.desc()).all()
        else:
            columns = Column.query.filter_by(phone=phone, father_id=fatherID) \
                .order_by(Column.time.desc()).all()
    else:
        if fatherID is 0:
            columns = Column.query.filter_by(phone=phone,
                                             type=columnType) \
                .order_by(Column.time.desc()).all()
        else:
            columns = Column.query.filter_by(phone=phone,
                                             type=columnType,
                                             father_id=fatherID) \
                .order_by(Column.time.desc()).all()

    datas = []
    for column in columns:
        data = {"id": column.id,
                "name": column.name,
                "introduction": column.introduction,
                "time": column.time,
                "phone": column.accounts,
                "picture": column.picture,
                "type": column.type,
                "child": getChildColumn(column.child)
                }
        datas.append(data)
    return json.dumps(sendData(True, datas, 'OK'))


"""
栏目旗下的子栏目
"""


def getChildColumn(modules):
    datas = []
    for module in modules:
        data = {"id": module.id,
                "name": module.name,
                "introduction": module.introduction,
                "phone": module.phone,
                "time": module.time,
                "picture": module.picture,
                "type": module.type
                }
        datas.append(data)
    return datas


"""
设置栏目
@ name: 名称
@ time: 时间
@ phone： 注册人
@ introduction： 内容
@ columnType：0 创造 1 制作
@ father_id ：父ID
@ picture： 附件照片
"""


@api.route('/api/setColumn', methods=['POST', 'GET'])
@login_required
def setColumn():
    name = request.values.get('name', type=str)
    introduction = request.values.get('introduction', type=str)
    currentTime = getCurrentDateTime()
    phone = current_user.get_id()
    picture = saveRequestFile('picture', 'photos/avatar')
    columnType = request.values.get('columnType', type=int)
    father_id = request.values.get('father_id', type=int)
    column = Column(name=name, introduction=introduction, time=currentTime,
                    phone=phone, picture=picture, type=columnType,
                    father_id=father_id)
    db.session.add(column)
    db.session.commit()
    return json.dumps(sendData(True, "提交成功", "OK"))


"""
设置子栏目
"""


@api.route('/api/setChildColumn', methods=['POST', 'GET'])
@login_required
def setChildColumn():
    name = request.values.get('name', type=str)
    introduction = request.values.get('introduction', type=str)
    currentTime = getCurrentDateTime()
    phone = current_user.get_id()
    picture = saveRequestFile('picture', 'photos/avatar')
    columnType = request.values.get('columnType', type=int)
    father_id = request.values.get('father_id', type=int)
    column = ChildColumn(name=name, introduction=introduction, time=currentTime,
                         phone=phone, picture=picture, type=columnType,
                         father_id=father_id)
    db.session.add(column)
    db.session.commit()
    return json.dumps(sendData(True, "提交成功", "OK"))


"""
获取栏目内容
@ columnID  
@ columnType
"""


@api.route('/api/getColumnContent', methods=['POST', 'GET'])
@login_required
def getColumnContent():
    columnID = request.values.get('columnID', default=None, type=str)
    columnType = request.values.get('columnType', type=int)
    if columnID is None:
        contents = Content.query.filter_by(Content.type is columnType) \
            .order_by(Content.time.desc()).all()
    else:
        contents = Content.query.filter_by(Content.father_identity is columnID and
                                           Content.type is columnType) \
            .order_by(Content.time.desc()).all()
    return json.dumps(sendData(True, SQLToData(contents), 'OK'))


"""
设置栏目内容
"""


@api.route('/api/setColumnContent', methods=['POST', 'GET'])
@login_required
def setColumnContent():
    name = request.values.get('name')
    subitile = request.values.get('subtitle')
    content_details = request.values.get('content')
    time = getCurrentDateTime()
    phone = current_user.get_id()
    photo = saveRequestFile('photo')
    video = saveRequestFile('video')
    audio = saveRequestFile('audio')
    visition = request.values.get('visition', type=bool)
    view_type = request.values.get('viewType')
    rich_text = request.values.get('rich_text')
    type = request.values.get('type')
    father_id = request.values.get('fatherID')
    content = Content(name=name, subitile=subitile, content_details=content_details,
                      time=time, phone=phone, photo=photo, video=video, audio=audio,
                      visition=visition, view_type=view_type, rich_tetx=rich_text,
                      type=type, father_id=father_id)
    db.session.add(content)
    db.session.commit()


"""
获取提问
"""

"""
提问旗下回答
"""

"""
获取验证码
"""


def getVerificationCode():
    arr = [str(i) for i in range(10)]
    myCode = random.sample(arr, 6)
    return ''.join(myCode)


"""
发送短信
"""


def sendMSM(phone, number):
    params = "{\"number\":\"" + number + "\"}"
    return aliyun_MSM.send_sms(uuid.uuid1(), phone, "觉他", "SMS_75765163", params)


def sendData(Flag, data, Message):
    return {
        "Flag": Flag,
        "data": data,
        "Message": Message
    }


def SQLToData(columns):
    data = []
    for content in columns:
        data.append(content.column_dict())
    return data


"""
获取当前时间
"""


def getCurrentDateTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


"""
保存照片
@ value request参数
@ fileUrl   文件存储路径
@ defaultUrl  没有文件使用默认文件路径 
"""


def saveRequestFile(value, fileUrl=None, defaultUrl=None):
    if value in request.files:
        for filename in request.files.getlist(value):
            filename = photos.save(filename, folder=fileUrl)
            file_url = photos.url(filename)
    else:
        file_url = defaultUrl
    return file_url


@login_manager.user_loader
def reload_user(username):
    token = request.values.get('token', type=str)
    user = UserInformation.verify_auth_token(token=token)
    if username == user:
        return UserInformation.query.filter_by(phone=user).first()
    else:
        return None
