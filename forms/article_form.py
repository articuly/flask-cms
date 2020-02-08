# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
                    SubmitField, BooleanField, \
                    SelectMultipleField,widgets,\
                    RadioField, SelectField,TextAreaField,\
                    HiddenField,IntegerField

from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length, \
                               EqualTo, Regexp

from models import  Category

class ArticleForm(FlaskForm):
    # coerce 表示选项值强制转换为int类型
    cate = SelectField("文章分类",coerce = int,
                       validators=[DataRequired()],
                       render_kw={"class":"form-control"})
    title = StringField("文章标题",
                        validators=[DataRequired()],
                        render_kw={"class": "form-control"})
    thumb = HiddenField("")
    intro = TextAreaField("文章简介",
                        validators=[DataRequired()],
                        render_kw={"class": "form-control"})
    content = TextAreaField("文章内容",
                        validators=[DataRequired()],
                        render_kw={"class": "form-control"})


class ArticleSearchForm(FlaskForm):
    q = StringField("关键字",
                    validators=[DataRequired()],
                    render_kw={"class":"form-control"})
    field = SelectField("查询字段",
                        choices=[("title", "按照标题查找"),
                                 ("content", "按照内容查找")],
                        render_kw={"class":"form-control"}

                        )
    order = SelectField("排序",
                        choices=[("1","按照id升序"),
                                 ("2", "按照id降序")],
                        render_kw={"class":"form-control"}
                    )


class CommentForm(FlaskForm):
    comment = TextAreaField("发表评论",
                            validators=[DataRequired()],
                            render_kw={"class":"form-control"}
                            )
    article_id = IntegerField("文章id",
                              validators=[DataRequired()]
                              )