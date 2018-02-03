from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail             #邮箱
from flask_moment import Moment
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from config import config
import os

db = SQLAlchemy()
auth = HTTPBasicAuth()
# 创建实例
login_manager = LoginManager()
# LoginManager 对象的 session_protection 属性可以设为 None 、 'basic' 或 'strong'设为 'strong' 时,Flask-Login 会记录客户端
# IP地址和浏览器的用户代理信息,如果发现异动就登出用户。
login_manager.session_protection = 'strong'


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])  # 根据传入参数，选择配置
    config[config_name].init_app(app)  # 传入当前项目实例，配置项目

    db.init_app(app)
    login_manager.init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_perfix="/api/v1.0")

    return app
