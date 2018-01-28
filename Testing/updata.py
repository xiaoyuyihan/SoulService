# -*- coding: utf-8 -*-
import os
from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, IMAGES,\
 patch_request_class

app = Flask(__name__)
url=os.getcwd()
app.config['UPLOADED_PHOTOS_DEST'] = url   # 文件储存地址

# 创建一个set（通过实例化UploadSet()类实现），
# 使用configure_uploads()方法注册并完成相应的配置（类似大多数扩展提供的初始化类）
"""
这里的photos是set的名字，它很重要。因为接下来它就代表你已经保存的文件，
对它调用save()方法保存文件，对它调用url()获取文件url，对它调用path()获取文件的绝对地址……
（你可以把它类比成代表数据库的db）"""
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app, 16*1024*1024)  # 文件大小限制，默认为16MB

html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>图片上传</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=photo>
         <input type=submit value=上传>
    </form>
    '''


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and 'photo' in request.files:
        for filename in request.files.getlist('photo'):
            filename = photos.save(filename, folder='demo_dir')
            file_url = photos.url(filename)
        return html + '<br><img src=' + file_url + '>'
    return html


if __name__ == '__main__':
    app.run()