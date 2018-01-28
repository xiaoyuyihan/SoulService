from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])  # 根据传入参数，选择配置
    config[config_name].init_app(app)  # 传入当前项目实例，配置项目

    db.init_app(app)
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_perfix="/api/v1.0")

    return app
