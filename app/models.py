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
    __tablename__ = 'user_information'
    id = db.Column(db.INT, primary_key=True)
    phone = db.Column(db.VARCHAR)
    email = db.Column(db.VARCHAR)
    username = db.Column(db.VARCHAR)
    password_hash = db.Column(db.VARCHAR)
    avatar = db.Column(db.VARCHAR)
    user_status = db.Column(db.SMALLINT)
    sex = db.Column(db.SMALLINT)
    birthday = db.Column(db.DATE)
    login_state = db.Column(db.SMALLINT)
    uuid = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    interest = db.Column(db.VARCHAR)
    address = db.Column(db.VARCHAR)
    permissions = db.Column(db.Integer)

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
    __tablename__ = 'user_registered'
    id = db.Column(db.INT, primary_key=True)
    phone = db.Column(db.VARCHAR)
    sourceint = db.Column(db.SMALLINT)
    registered_time = db.Column(db.DATETIME)


"""
登录表
"""


class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.INT, primary_key=True)
    phone = db.Column(db.VARCHAR)
    login_ip = db.Column(db.VARCHAR)
    login_time = db.Column(db.DATETIME)
    longitude = db.Column(db.VARCHAR)
    login_mode = db.Column(db.INT)
    location = db.Column(db.VARCHAR)
    latitude = db.Column(db.VARCHAR)
    state = db.Column(db.INT)
    user_id = db.Column(db.Integer)


"""
喜爱表
"""


class Preferences(db.Model):
    __tablename__ = 'preference'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.VARCHAR)
    subject = db.Column(db.VARCHAR)
    description = db.Column(db.VARCHAR)
    time = db.Column(db.DATETIME)


"""
打赏表
"""


class Bounty(db.Model):
    __tablename__ = 'bounty'
    id = db.Column(db.Integer, primary_key=True)


"""
用户日志表
"""


class Log(db.Model):
    __tablename__ = 'log'
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
    __tablename__ = 'collection'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content_id = db.Column(db.Integer)
    content_type = db.Column(db.Integer)
    time = db.Column(db.DATETIME)
    phone = db.Column(db.VARCHAR)


"""
用户行为表
"""


class Behavior(db.Model):
    __tablename__ = 'behavior'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.DATETIME)
    frequency = db.Column(db.Integer)


"""
验证码表
"""


class ValidateCode(db.Model):
    __tablename__ = 'validate_code'
    id = db.Column(db.Integer, primary_key=True)
    validate = db.Column(db.VARCHAR)
    time = db.Column(db.INT)
    phone = db.Column(db.VARCHAR)
    standard_time = db.Column(db.VARCHAR)
    state = db.Column(db.VARCHAR)
    message = db.Column(db.VARCHAR)


"""
学习专业
"""


class Major(db.Model):
    __tablename__ = 'major'
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
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    identity = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    founder = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    picture = db.Column(db.VARCHAR)
    father_identity = db.Column(db.INT, db.ForeignKey('major.identity'))


"""
栏目表
"""


class Column(db.Model):
    __tablename__ = 'column'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    push_time = db.Column(db.DATETIME)
    column_interval = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    accounts = db.Column(db.VARCHAR, db.ForeignKey('user_information.phone'))  # 创建者
    praise = db.Column(db.INT)
    father_identity = db.Column(db.INT)
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
    __tablename__ = 'child_column'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    state = db.Column(db.SMALLINT)
    location = db.Column(db.INT)
    praise = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    number = db.Column(db.INT)
    father_id = db.Column(db.INT, db.ForeignKey('column.id'))


"""
栏目内容表
"""


class ColumnContent(db.Model):
    __tablename__ = 'column_content'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR)
    subtitle = db.Column(db.VARCHAR)
    content_details = db.Column(db.TEXT)
    time = db.Column(db.DATETIME)
    accounts = db.Column(db.VARCHAR)
    photo = db.Column(db.VARCHAR)
    video = db.Column(db.VARCHAR)
    audio = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    visition = db.Column(db.SMALLINT)
    type = db.Column(db.INT)
    richtext = db.Column(db.TEXT)
    live = db.Column(db.INT)
    father_id = db.Column(db.INT, db.ForeignKey('childColumn.id'))

    def column_dict(self):
        self.time = str(self.time)
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict


"""
DIY方向表
"""


class Orientation(db.Model):
    __tablename__ = 'orientation'
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
    __tablename__ = 'description'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    identity = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    founder = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    picture = db.Column(db.VARCHAR)
    father_identity = db.Column(db.INT, db.ForeignKey('orientation.identity'))


"""
制造栏目
"""


class Manufacturer(db.Model):
    __tablename__ = 'manufacturer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    time = db.Column(db.DATETIME)
    founder = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    phone = db.Column(db.VARCHAR)
    chlid = db.RelationshipProperty('ChildManufacturer')


"""
子制造栏目
"""


class ChildManufacturer(db.Model):
    __tablename__ = 'child_manufacturer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    number = db.Column(db.INT)
    time = db.Column(db.DATETIME)
    founder = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    introduction = db.Column(db.VARCHAR)
    picture = db.Column(db.VARCHAR)
    father_identity = db.Column(db.INT, db.ForeignKey('manufacturer.id'))


"""
制造内容表
"""


class ManufacturerContent(db.Model):
    __tablename__ = 'manufacturer_content'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR)
    subtitle = db.Column(db.VARCHAR)
    content_details = db.Column(db.TEXT)
    time = db.Column(db.DATETIME)
    accounts = db.Column(db.VARCHAR)
    photo = db.Column(db.VARCHAR)
    video = db.Column(db.VARCHAR)
    audio = db.Column(db.VARCHAR)
    url = db.Column(db.VARCHAR)
    visition = db.Column(db.SmallInteger)
    type = db.Column(db.INT)
    richtext = db.Column(db.TEXT)
    father_id = db.Column(db.INT, db.ForeignKey('childManufacturer.id'))
    live = db.Column(db.INT)

    def column_dict(self):
        self.time = str(self.time)
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict


"""
问题表
"""


class Problem(db.Model):
    __tablename__ = 'problem'
    id = db.Column(db.INT, primary_key=True)
    user = db.Column(db.VARCHAR)
    content = db.Column(db.VARCHAR)
    time = db.Column(db.DATETIME)
    picture = db.Column(db.VARCHAR)
    video = db.Column(db.VARCHAR)
    audio = db.Column(db.VARCHAR)
    number = db.Column(db.INT)
    answer = db.RelationshipProperty('Answer')


"""
回答表
"""


class Answer(db.Model):
    __tablename__ = 'answer'
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
    __tablename__ = 'comments'
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
    __tablename__ = 'concerns'
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
    __tablename__ = 'message'
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
    __tablename__ = 'update'
    id = db.Column(db.INT, primary_key=True)


"""
系统日志表
"""


class Diary(db.Model):
    __tablename__ = 'diary'
    id = db.Column(db.INT, primary_key=True)
