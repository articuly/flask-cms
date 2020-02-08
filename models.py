# -*- coding=utf-8 -*-
from libs import db
from datetime import datetime
from werkzeug.security import generate_password_hash, \
                              check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    realname = db.Column(db.String)
    sex = db.Column(db.Integer)
    mylike = db.Column(db.String)
    city = db.Column(db.String)
    intro = db.Column(db.String)

    def hash_password(self,password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    thumb = db.Column(db.String)
    intro = db.Column(db.String)
    content = db.Column(db.Text)
    author = db.Column(db.String)
    is_recommend = db.Column(db.Integer)
    pubdate = db.Column(db.DateTime, default=datetime.utcnow)
    cate_id = db.Column(db.Integer, db.ForeignKey("category.cate_id"))
    comments = db.relationship("Comment", back_populates='article', cascade='all, delete-orphan')

class Category(db.Model):
    cate_id = db.Column(db.Integer, primary_key=True)
    # unique=True,表示此字段值不能重复
    cate_name = db.Column(db.String, unique=True)
    cate_order = db.Column(db.Integer, default=0)
    articles = db.relationship("Article")

class Comment(db.Model):
    '''
    评论模型

    '''
    comment_id = db.Column(db.Integer, primary_key=True)
    observer = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    article = db.relationship('Article', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    # 自引用
    replied = db.relationship('Comment', back_populates='replies', remote_side=[comment_id])
    # Same with:
    # replies = db.relationship('Comment', backref=db.backref('replied', remote_side=[id]),
    # cascade='all,delete-orphan')
