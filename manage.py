# manage.py 用于启动程序以及其他的程序任务。
import os
from app import create_app
from flask_uploads import UploadSet, configure_uploads, IMAGES,\
 patch_request_class

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# 创建一个set（通过实例化UploadSet()类实现），
# 使用configure_uploads()方法注册并完成相应的配置（类似大多数扩展提供的初始化类）
"""
这里的photos是set的名字，它很重要。因为接下来它就代表你已经保存的文件，
对它调用save()方法保存文件，对它调用url()获取文件url，对它调用path()获取文件的绝对地址……
（你可以把它类比成代表数据库的db）"""
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app, 16*1024*1024)  # 文件大小限制，默认为16MB


if __name__ == '__main__':
    app.run(host='0.0.0.0')