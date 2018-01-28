# 接口
import os

from . import api
from flask import request
import random
import time
from tool import aliyun_MSM
import uuid
from app.models import ValidateCode, Major, UserInformation, \
    UserRegistered, Login, Subject
from app import db
from manage import photos
import json

"""
测试
"""


@api.route('/', methods=['GET',"POST"])
def Test():
    return "SOUL"

"""
注册接口
"""


@api.route('/registered', methods=['POST'])
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
            file_url = os.getcwd()+'/photos/默认图片'
        username = request.values.get('username', default=None, type=str)  # 用户名
        password = request.values.get('password', default=None, type=str)  # 密码
        sourceint = request.values.get('sourceint', default=0, type=int)  # 注册来源
        registered_time = getCurrentDateTime()  # 注册时间
        user_status = request.values.get('status', default=0, type=int)  # 账户状态
        interest = request.values.get('interest', default=None, type=str)  # 兴趣点

        userRegistered = UserRegistered(phone=phone, sourceint=sourceint, registered_time=registered_time)
        userInformation = UserInformation(phone=phone, username=username, user_status=user_status,
                                          interest=interest, password=password, avatar=file_url)
        db.session.add(userRegistered)
        db.session.add(userInformation)
        db.session.commit()
        return json.dumps(sendData(True, "注册成功", 'OK'))
    else:
        return json.dumps(sendData(False, "该手机号已注册，如忘记密码请找回密码。", "ERROR_ACCOUNT_REGISTERED"))


"""
登录接口
"""


@api.route('/login', methods=['POST', 'GET'])
def login():
    phone = request.values.get('phone', default=None, type=str)
    password = request.values.get('password', default=None, type=str)
    login_time = getCurrentDateTime()
    login_ip = str(request.remote_addr)
    login_mode = request.values.get('mode', default=None, type=int)
    longitude = request.values.get('longitude', default='', type=str)
    latitude = request.values.get('latitude', default='', type=str)
    location = request.values.get('location', default='', type=str)
    loginModel = Login(phone=phone, login_time=login_time, login_ip=login_ip, login_mode=login_mode,
                       longitude=longitude, latitude=latitude, location=location)
    try:
        user = UserInformation.query.filter_by(phone=phone).first()
    except Exception as e:
        user = None
    if user is not None and user.verify_password(password):
        loginModel.state = 1
        data = json.dumps(sendData(True, "登陆成功", 'OK'))
    elif user is None:
        loginModel.state = 0
        data = json.dumps(sendData(False, "该帐号未注册，请注册后再次登录", 'ERROR_NO_USER'))

    else:
        loginModel.state = -1
        data = json.dumps(sendData(False, "密码错误，请确认密码后登录", 'ERROR_PASSWORD'))

    db.session.add(loginModel)
    db.session.commit()
    return data


"""
修改密码
"""


@api.route("/changePassword", methods=["POST", "GET"])
def changePassword():
    phone = request.values.get('phone', default=None, type=str)
    password = request.values.get('password', default=None, type=str)
    try:
        user = UserInformation.query.filter_by(phone=phone).first();
    except Exception as e:
        user = None
    if user is None:
        return json.dumps(sendData(False, "该手机号未注册", 'ERROR_NO_USER'))
    user.password = password
    return json.dumps(sendData(True, "修改完成,请登录", 'OK'))


"""
获取验证
"""


@api.route('/getVerification', methods=['POST', 'GET'])
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


@api.route('/getMajor', methods=['POST', 'GET'])
def getMajor():
    fathers = Major.query.all()
    datas = []
    for father in fathers:
        data = {"name": father.name,
                "identity": father.identity,
                "introduction": father.introduction,
                "child": getModuleContent(father.child)
                }
        datas.append(data)
    return json.dumps(sendData(True, datas, 'OK'))


"""
获取旗下专业学科
"""


def getModuleContent(modules):
    datas = []
    for module in modules:
        data = {"name": module.name,
                "identity": module.identity,
                "introduction": module.introduction,
                "picture": module.picture}
        datas.append(data)
    return datas


"""
获取某个学科下的栏目
"""

"""
栏目旗下的子栏目
"""

"""
获取栏目内容
"""

"""
获取DIY的方向
"""

"""
方向下的种类
"""

"""
用户创建的DIY栏目
"""
"""
DIY栏目子栏目
"""
"""
DIY 栏目内容
"""

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

"""
获取当前时间
"""


def getCurrentDateTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
