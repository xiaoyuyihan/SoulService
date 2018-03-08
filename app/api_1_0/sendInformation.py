from . import api
from flask import request
from flask_login import login_required, current_user
from app.models import Content, UserInformation, Column, \
    Preference, Problem
import json
from .information import sendData, SQLToData, ContentToData, ContentAddComment

"""
搜索
"""


@api.route('/api/search', methods=['POST', 'GET'])
@login_required
def Search():
    searchName = request.values.get('name', default="", type=str)
    Contents = Content.query.filter(
        Content.name.like("%" + searchName + "%") is not None
        or Content.subtitle.like("%" + searchName + "%")).all()
    ProblemContents = Problem.query.filter(
        Problem.content.like("%" + searchName + "%")).all()
    data = {
        'Contents': SQLToData(Contents),
        'ProblemContents': SQLToData(ProblemContents)
    }
    return json.dumps(sendData(True, data, 'OK'))


"""
最新
"""


@api.route('/api/newContent', methods=['POST', 'GET'])
@login_required
def NewContent():
    page = request.values.get('page', default=1, type=int)
    ColumnContents = Content.query.with_entities(Content.id,
                                                 Content.name,
                                                 Content.subtitle,
                                                 Content.time,
                                                 Content.content_details,
                                                 Content.phone,
                                                 Content.view_type,
                                                 Content.father_id,
                                                 Content.column_id,
                                                 Content.type,
                                                 Content.visition,
                                                 Content.photo,
                                                 Content.live,
                                                 Column.name,
                                                 Column.father_id,
                                                 UserInformation.username,
                                                 UserInformation.avatar) \
        .filter_by(visition=0) \
        .join(Column, Column.id == Content.column_id) \
        .join(UserInformation, UserInformation.phone == Content.phone) \
        .order_by(Content.time.desc()) \
        .paginate(page=page, per_page=25, error_out=False)
    return json.dumps(sendData(True, ContentToData(ContentAddComment(ColumnContents.items)), 'OK'))


"""
最热
"""


@api.route('/api/hotContent', methods=['POST', 'GET'])
@login_required
def HotContent():
    page = request.values.get('page', default=1, type=int)
    ColumnContents = Content.query.with_entities(Content.id,
                                                 Content.name,
                                                 Content.subtitle,
                                                 Content.time,
                                                 Content.content_details,
                                                 Content.phone,
                                                 Content.view_type,
                                                 Content.father_id,
                                                 Content.column_id,
                                                 Content.type,
                                                 Content.visition,
                                                 Content.photo,
                                                 Content.live,
                                                 Column.name,
                                                 Column.father_id,
                                                 UserInformation.username,
                                                 UserInformation.avatar) \
        .filter_by(visition=0) \
        .join(Column, Column.id == Content.column_id) \
        .join(UserInformation, UserInformation.phone == Content.phone) \
        .order_by(Content.live.desc()) \
        .paginate(page=page, per_page=25, error_out=False)
    return json.dumps(sendData(True, ContentToData(ContentAddComment(ColumnContents.items)), 'OK'))


"""
推荐
"""


@api.route('/api/recommended', methods=['POST', 'GET'])
@login_required
def Recommended():
    user = current_user.get_id()
    page = request.values.get('page', default=1, type=int)
    ColumnContents = Content.query.with_entities(Content.id,
                                                 Content.name,
                                                 Content.subtitle,
                                                 Content.time,
                                                 Content.content_details,
                                                 Content.phone,
                                                 Content.view_type,
                                                 Content.father_id,
                                                 Content.column_id,
                                                 Content.type,
                                                 Content.visition,
                                                 Content.photo,
                                                 Content.live,
                                                 Column.name,
                                                 Column.father_id,
                                                 UserInformation.username,
                                                 UserInformation.avatar) \
        .filter_by(visition=0) \
        .join(Preference, Content.father_id == Preference.child_column_id and
              Content.type == Preference.preference_type) \
        .filter_by(phone=user) \
        .join(Column, Column.id == Content.column_id) \
        .join(UserInformation, UserInformation.phone == Content.phone) \
        .order_by(Content.time.desc()) \
        .paginate(page=page, per_page=25, error_out=False)
    return json.dumps(sendData(True, ContentToData(ContentAddComment(ColumnContents.items)), 'OK'))
