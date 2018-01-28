from flask import Blueprint

api = Blueprint('api', __name__)

from . import information
from . import sendInformation
from . import obtainInformation
