from flask import Flask, render_template
from flask import request, redirect, url_for
from libs import db, ckeditor, csrf, dropzone
from views.users import user_app
from views.articles import article_app
from views.upload import upload_app
from flask_migrate import Migrate
from models import Category, User
from flask import session
from admin import admin_app
from member import member_app
from sqlalchemy import MetaData
from settings import config
from forms.account_form import LoginForm


app = Flask(__name__)
app.config.from_object(config['development'])


db.init_app(app)
ckeditor.init_app(app)
csrf.init_app(app)
dropzone.init_app(app)

app.register_blueprint(user_app, url_prefix="/user")
app.register_blueprint(article_app, url_prefix="/article")
app.register_blueprint(upload_app, url_prefix="/upload")
app.register_blueprint(admin_app, url_prefix="/admin")
app.register_blueprint(member_app, url_prefix="/member")

@app.route('/')
def index():
    return render_template("index.html" )

#
@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    message = None
    # if request.method == "POST":
    if  form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        user = User.query.filter_by(username=username).first()
        if user and user.validate_password(password):
            session['user'] = user.username
        # 登录成功返回首页
            return redirect(url_for("index"))
        else:
            message = "用户名与密码不匹配"
    else:
        print(form.errors)

    #登录失败，给出提示
    return render_template("login.html", message=message,
                            form=form
                           )


@app.route("/logout")
def logout():
    if session.get('user'):
        session.pop("user")

    return redirect(url_for("index"))


@app.context_processor
def account():
    username = session.get('user')
    return {"username":username}

@app.context_processor
def getCateList():
    cates = Category.query.all()
    return {"cates":cates}



# 添加render_as_batch=True
# SQLite支持批处理修改
# 但是这种如果修改多个字段，可能在发生错误时，发生修改不一致

migrate = Migrate(app,db,render_as_batch=True)