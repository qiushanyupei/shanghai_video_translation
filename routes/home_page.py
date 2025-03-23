from flask import Blueprint,render_template,request,jsonify
from db.db_init import get_db
import os
from db.db_table import Video,User

home = Blueprint('home', __name__)

@home.route('/',methods=['GET','POST'])
def home_page():
    if request.method == 'POST':
        file = request.files['file']
        # 保存文件到指定目录
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        #还需要通过username查找出user_id

        with get_db() as db:
            user = db.query(User).filter(User.username == username).first()

            new_file = Video(user_id = user.id,filename=file_name,filepath=file_path)
            # 添加到会话
            db.add(new_file)
            # 提交会话，将数据保存到数据库
            db.commit()
            return jsonify({"flag": "Success", "file_id": new_file.id})

    return render_template("主界面.html")