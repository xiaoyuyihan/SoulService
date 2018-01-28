from . import api
from flask import request, send_from_directory
import json
from .information import sendData
import hashlib


@api.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(api.config['UPLOAD_FOLDER'],
                               filename)