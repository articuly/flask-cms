from flask import Flask, render_template
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my.db"

db=SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html" )


@app.route('/login', methods=['get', 'post'])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
    print(username, password)
    return render_template("login.html")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    realname = db.Column(db.String)
    sex = db.Column(db.Integer)
    mylike = db.Column(db.String)
    city = db.Column(db.String)
    intro = db.Column(db.String)

@app.route("/register", methods=['get','post'])
def register():
    if request.method == "POST":
        realname = request.form['name']
        username = request.form['username']
        password = request.form['password']
        sex      = request.form['sex']
        mylike   = '|'.join(request.form.getlist('like'))
        city     = request.form['city']
        intro    = request.form['intro']
        user = User(realname=realname,
                    username=username,
                    password=password,
                    sex=sex,
                    mylike=mylike,
                    city=city,
                    intro=intro)


        db.session.add(user)
        db.session.commit()

    return render_template("register.html")


@app.context_processor
def account():
    username = None
    return {"username":username}


# 获得用户列表
@app.route("/userlist", methods=['get', "post"])
def userList():
    if request.method == "POST":
        q = request.form['q']
        condition = {request.form['field']:q}
        #filter_by
        # users = User.query.filter_by(**condition).all()
        # filter
        # like
        if request.form['field'] == "realname":
            condition = User.realname.like('%%%s%%' % q)
        else:
            condition = User.username.like('%%%s%%' % q)
        if request.form['order'] == "1":
            order = User.id.asc()
        else:
            order = User.id.desc()

        users = User.query.filter(condition, User.sex==request.form['sex']).order_by(order).all()

    else:
        # users = User.query.all()
        page = request.args.get('page')
        users = User.query.paginate(int(page),10)


    return render_template("user/user_list.html", users=users.items,
                           pages=users.pages,
                           total=users.total,
                           pageList=users.iter_pages()
                           )


# 根据用户id删除用户
@app.route("/user_delete/<int:user_id>")
def deleteUser(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("userList"))


# 用户信息修改
@app.route("/useredit/<int:user_id>", methods=['get', 'post'])
def editUser(user_id):
    user = User.query.get(user_id)
    if request.method == "POST":
        user.username = request.form['username']
        user.realname = request.form['name']
        user.sex = request.form['sex']
        user.mylike = "|".join(request.form.getlist('like'))
        user.city = request.form['city']
        user.intro = request.form['intro']
        db.session.commit()
        return redirect(url_for("userList"))
    return render_template("user/edit_user.html", user=user)


def createBatchUsers():
    words = list("abcdefghijklmnopqrstuvwxyz")
    citys = ["010", "021", "0512"]
    mylikes = ["睡觉","旅游", "看书", "唱歌"]
    import random

    for i in range(100):
        random.shuffle(words)
        username = "".join(words[:6])
        sex = random.randint(0,1)
        city = citys[random.randint(0,2)]
        random.shuffle(mylikes)
        mylike = "|".join(mylikes[:random.randint(0,3)])
        user = User(realname="-",
                    username=username,
                    password="",
                    sex=sex,
                    mylike=mylike,
                    city=city,
                    intro="")
        db.session.add(user)
    db.session.commit()