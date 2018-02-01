# config.py 存储配置；
import os

basedir = os.path.abspath(os.path.dirname(__file__))


# 通用配置类
class Config:
    # 通过环境变量导入，安全灵活（设置默认值，防止环境中没有定义）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = 'Flasky'
    FLASKY_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    UPLOADED_PHOTOS_DEST = os.getcwd()

    # 对当前环境的配置初始化
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    MAIL_SERVER = 'smtp.sina.cn'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:lunhui1995@localhost:3306/soul_sql'


class TestingConfig(Config):
    TESTING = True
    # 每个环境都使用不同的数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') \
                              or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}