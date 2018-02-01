"""
SQL db
"""
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

"""
用户资料表
"""


class UserInformation(db.Model):
    __table_name__ = 'user_information'
    id = db.Column(db.INT, primary_key=True)
    phone = db.Column(db.VARCHAR)               # 手机号
    email = db.Column(db.VARCHAR)               # 邮箱
    username = db.Column(db.VARCHAR)            # 用户名
    password_hash = db.Column(db.VARCHAR)       # 加密后密码
    avatar = db.Column(db.VARCHAR)              # 头像路径
    user_status = db.Column(db.SMALLINT)        # 用户状态
    sex = db.Column(db.SMALLINT)                # 性别
    birthday = db.Column(db.DATE)               # 生日
    login_state = db.Column(db.SMALLINT)        # 登录状态
    uuid = db.Column(db.VARCHAR)                # 客户端唯一标识位
    introduction = db.Column(db.VARCHAR)        # 个人介绍
    address = db.Column(db.VARCHAR)             # 地址
    permissions = db.Column(db.Integer)         # 权限

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


"""
用户注册表
"""


class UserRegistered(db.Model):
    __table_name__ = 'user_registered'
    id = db.Column(db.INT, primary_key=True)
    phone = db.Column(db.VARCHAR)                   # 手机号
    sourceint = db.Column(db.SMALLINT)              # 用户注册来源(0->iPhone, 1->iPad, 2->Android, 3->微信, 4->H5, 5->网站，6->未知)'
    registered_time = db.Column(db.DATETIME)        # 注册时间


"""
登录表
"""


class Login(db.Model):
    __table_name__ = 'login'
    id = db.Column(db.INT, primary_key=True)
    phone = db.Column(db.VARCHAR)                  # 手机号
    login_ip = db.Column(db.VARCHAR)               # 登录IP
    login_time = db.Column(db.DATETIME)            # 登陆时间
    longitude = db.Column(db.VARCHAR)              # 登录经度
    login_mode = db.Column(db.INT)                 # 登录方式  1.Android 2.IOS 3.其他 4.web
    location = db.Column(db.VARCHAR)               # 登陆地址
    latitude = db.Column(db.VARCHAR)               # 登陆纬度
    state = db.Column(db.INT)                      # 登录状态 -1-密码错误 0-无账户 1-成功
    user_id = db.Column(db.Integer)                # 唯一ID


"""
喜爱表
"""


class Preference(db.Model):
    __table_name__ = 'preference'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.VARCHAR)                   # 手机号
    child_column_id = db.Column(db.INT)             # 栏目ID
    found_time = db.Column(db.DATETIME)                   # 时间
    preference_type = db.Column(db.INT)                        # 类型    0 学习  1 创造


"""
打赏表
"""


class Bounty(db.Model):
    __table_name__ = 'bounty'
    id = db.Column(db.Integer, primary_key=True)


"""
用户日志表
"""


class Log(db.Model):
    __table_name__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.VARCHAR)
    time = db.Column(db.DATETIME)
    platform = db.Column(db.Integer)
    content = db.Column(db.VARCHAR)
    platform_content = db.Column(db.VARCHAR)


"""
收藏表
"""


class Collection(db.Model):
    __table_name__ = 'collection'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.INT)
    content_id = db.Column(db.INT)
    content_type = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    phone = db.Column(db.VARCHAR)


"""
用户行为表
"""


class Behavior(db.Model):
    __table_name__ = 'behavior'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.DATETIME)
    frequency = db.Column(db.Integer)
    phone = db.Column(db.VARCHAR)


"""
验证码表
"""


class ValidateCode(db.Model):
    __table_name__ = 'validate_code'
    id = db.Column(db.Integer, primary_key=True)
    validate = db.Column(db.VARCHAR)                # 验证码
    time = db.Column(db.INT)
    phone = db.Column(db.VARCHAR)
    standard_time = db.Column(db.VARCHAR)
    state = db.Column(db.VARCHAR)                   # 状态
    message = db.Column(db.VARCHAR)                 # 返回消息


"""
学习专业
"""


class Major(db.Model):
    __table_name__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    identity = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    founder = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    picture = db.Column(db.VARCHAR)
    child = db.RelationshipProperty('Subject')


"""
科目表
"""


class Subject(db.Model):
    __table_name__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    identity = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    founder = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    picture = db.Column(db.VARCHAR)
    father_id = db.Column(db.INT, db.ForeignKey('major.identity'))


"""
DIY方向表
"""


class Orientation(db.Model):
    __table_name__ = 'orientation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    identity = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    founder = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    picture = db.Column(db.VARCHAR)
    child = db.RelationshipProperty('Description')


"""
DIY种类表
"""


class Description(db.Model):
    __table_name__ = 'description'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    identity = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    founder = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    picture = db.Column(db.VARCHAR)
    father_id = db.Column(db.INT, db.ForeignKey('orientation.identity'))


"""
栏目表
"""


class Column(db.Model):
    __table_name__ = 'column'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR)                                    # 栏目名
    introduction = db.Column(db.VARCHAR)                            # 介绍
    push_time = db.Column(db.DATETIME)
    column_interval = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    phone = db.Column(db.VARCHAR, db.ForeignKey('user_information.phone'))  # 创建者
    praise = db.Column(db.INT)
    father_id = db.Column(db.INT)
    picture = db.Column(db.VARCHAR)
    type = db.Column(db.INT)                                         # 类型 0：学习，1：创造
    child = db.RelationshipProperty('ChildColumn')

    def column_dict(self):
        self.time = str(self.time)
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict


"""
子栏目表
"""


class ChildColumn(db.Model):
    __table_name__ = 'child_column'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR)                                    # 栏目名
    introduction = db.Column(db.VARCHAR)                            # 介绍
    state = db.Column(db.SMALLINT)
    location = db.Column(db.INT)
    praise = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    number = db.Column(db.INT)
    picture = db.Column(db.VARCHAR)                                 # 图片路径
    type = db.Column(db.INT)                                        # 类型 0：学习，1：创造
    father_id = db.Column(db.INT, db.ForeignKey('column.id'))


"""
栏目内容表
"""


class Content(db.Model):
    __table_name__ = 'content'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR)                            # 标题
    subtitle = db.Column(db.VARCHAR)                        # 副标题
    content_details = db.Column(db.TEXT)                    # 内容详情
    time = db.Column(db.DATETIME)                           # 创建时间
    phone = db.Column(db.VARCHAR)                           # 创建人
    photo = db.Column(db.VARCHAR)                           #
    video = db.Column(db.VARCHAR)
    audio = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    visition = db.Column(db.SMALLINT)                       # 是否可见
    view_type = db.Column(db.INT)                           # 视图类型
    rich_text = db.Column(db.TEXT)
    live = db.Column(db.INT)
    type = db.Column(db.INT)                                # 类型 0 学习 1制造
    father_id = db.Column(db.INT, db.ForeignKey('child_column.id'))

    def column_dict(self):
        self.time = str(self.time)
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict


"""
问题表
"""


class Problem(db.Model):
    __table_name__ = 'problem'
    id = db.Column(db.INT, primary_key=True)
    user = db.Column(db.VARCHAR)                # 提问人
    content = db.Column(db.VARCHAR)             # 内容
    time = db.Column(db.DATETIME)               # 时间
    picture = db.Column(db.VARCHAR)             # 图片
    video = db.Column(db.VARCHAR)               #
    audio = db.Column(db.VARCHAR)
    number = db.Column(db.INT)
    problem = db.Column(db.INT)                 # 来源
    answer = db.RelationshipProperty('Answer')


"""
回答表
"""


class Answer(db.Model):
    __table_name__ = 'answer'
    id = db.Column(db.INT, primary_key=True)
    user = db.Column(db.VARCHAR)
    content = db.Column(db.VARCHAR)
    time = db.Column(db.DATETIME)
    agree = db.Column(db.INT)
    not_agree = db.Column(db.INT)
    question_id = db.Column(db.INT, db.ForeignKey('problem.id'))


"""
评价表
"""


class Comments(db.Model):
    __table_name__ = 'comments'
    id = db.Column(db.INT, primary_key=True)
    accounts = db.Column(db.VARCHAR)
    time = db.Column(db.DATETIME)
    identity = db.Column(db.INT)
    praise = db.Column(db.INT)
    content = db.Column(db.VARCHAR)
    type = db.Column(db.INT)


"""
关注表
"""


class Concerns(db.Model):
    __table_name__ = 'concerns'
    id = db.Column(db.INT, primary_key=True)
    concern_id = db.Column(db.INT)
    type = db.Column(db.INT)
    phone = db.Column(db.VARCHAR)
    time = db.Column(db.DATETIME)
    source = db.Column(db.VARCHAR)


"""
消息表
"""


class Message(db.Model):
    __table_name__ = 'message'
    id = db.Column(db.INT, primary_key=True)
    sendID = db.Column(db.VARCHAR)
    acceptID = db.Column(db.VARCHAR)
    message = db.Column(db.VARCHAR)
    time = db.Column(db.DATETIME)
    type = db.Column(db.INT)
    is_read = db.Column(db.BOOLEAN)


"""
版本更新
"""


class Update(db.Model):
    __table_name__ = 'update'
    id = db.Column(db.INT, primary_key=True)


"""
系统日志表
"""


class Diary(db.Model):
    __table_name__ = 'diary'
    id = db.Column(db.INT, primary_key=True)
