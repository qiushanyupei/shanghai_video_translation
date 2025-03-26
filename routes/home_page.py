from flask import Blueprint,render_template,request,jsonify,url_for
from db.db_init import get_db
import os
from db.db_table import Video,User
from model.const import *

home = Blueprint('home', __name__)

@home.route('/',methods=['GET','POST'])
def home_page():
    if request.method == 'POST':
        file = request.files['file']#有request.files和request.form两种形式，前端和后端交互时由Flask区分
        username = request.form.get('username')
        # 转换为绝对路径
        absolute_path = os.path.join(os.path.join(os.path.dirname(__file__), "..", UPLOAD),file.filename)
        # print(os.path.dirname(__file__))
        # print(os.path.join(os.path.dirname(__file__), "..", UPLOAD))
        # print(absolute_path)
        # print(os.path.join(os.path.join(os.path.dirname(__file__), ".", UPLOAD),file.filename))
        # 保存文件到指定目录
        file.save(absolute_path)
        new_path = os.path.join(UPLOAD, file.filename).replace("static/", "").replace("\\","/")
        new_path = url_for("static", filename=new_path)
        print(new_path)
        #还需要通过username查找出user_id
        with get_db() as db:
            user = db.query(User).filter(User.username == username).first()
            new_file = Video(user_id = user.id,filename=file.filename,filepath=new_path)
            # 添加到会话
            db.add(new_file)
            # 提交会话，将数据保存到数据库
            db.commit()
            return jsonify({"flag": "Success", "file_path": new_file.filepath})

    return render_template("主界面.html")