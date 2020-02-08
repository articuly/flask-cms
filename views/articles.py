# -*- coding=utf-8 -*-

from flask import request, redirect, url_for, render_template
from libs import db, login_required
from models import Article, Category, Comment
from flask import Blueprint, jsonify
from forms.article_form import CommentForm
from utils import queryObjToDicts

article_app = Blueprint("article_app", __name__)

# 根据文章id阅读文章
@article_app.route("/view/<int:article_id>")
def view(article_id):
    article = Article.query.get_or_404(article_id)
    form = CommentForm()
    if  not article:
        return redirect(url_for(".list"))
    return render_template("article/detail.html", article=article, form=form, article_id=article_id)

# 评论列表
@article_app.route("/comment")
def getComments():
    article_id = request.args.get('article_id')
    print("q=",request.args.get('q'))
    if article_id:
        article_id = int(article_id)
        page = int(request.args.get('page', 1))
        res = Comment.query.filter_by(article_id=article_id).order_by( Comment.timestamp.desc()).paginate(page,10)
        if res.items:

            comments = queryObjToDicts(res.items,['body', 'observer', 'timestamp'])
            return jsonify({"res":"success", "comments":comments, "next_page":res.next_num, "pages":res.pages})
    return jsonify({"res":"fail"})

# 根据文章cate_id显示文章列表
@article_app.route("/cate/<int:cate_id>/<int:page>")
@article_app.route("/", defaults={"cate_id":0, "page":1})
def getArticleList(cate_id, page):
    if cate_id == 0:
        res = Article.query.paginate(page, 20)
    else:
        res = Article.query.filter_by(cate_id=cate_id).paginate(page,20)
    articles = res.items
    pageList = res.iter_pages()
    return render_template("index.html",
                            articles=articles,
                            pageList=pageList
                           )



