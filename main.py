# -*- coding: utf8 -*-
#
# flask demo for wangEditor
#
__author__  = "Mr.tao"
__email__   = "staugur@saintic.com"
__website__ = "www.saintic.com"

import os
from flask import Flask, render_template, Response, request
from werkzeug import secure_filename

app = Flask(__name__)

IMAGE_UPLOAD_DIR   = 'static/img/ImageUploads/'
UPLOAD_FOLDER      = os.path.join(os.path.dirname(os.path.abspath(__file__)), IMAGE_UPLOAD_DIR)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#文件名合法性验证
allowed_file = lambda filename: '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("blogWrite.html")

#对图片上传进行响应
@app.route("/uploadimage/", methods=["POST",])
def UploadImage():
    app.logger.debug(request.files)
    f = request.files.get("WriteBlogImage")
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        filedir  = os.path.join(app.root_path, UPLOAD_FOLDER)
        if not os.path.exists(filedir): os.makedirs(filedir)
        app.logger.debug(filedir)
        f.save(os.path.join(filedir, filename))
        imgUrl = request.url_root + IMAGE_UPLOAD_DIR + filename
        res =  Response(imgUrl)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
    else:
        result = r"error|未成功获取文件，上传失败"
        res =  Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res

@app.route("/test/")
def GetImage():
    return """<html><body>
<form action="/uploadimage/" method="post" enctype="multipart/form-data" name="upload_form">
  <label>选择图片文件</label>
  <input name="WriteBlogImage" type="file" accept="image/gif, image/jpeg"/>
  <input name="upload" type="submit" value="上传" />
</form>
</body></html>"""


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)