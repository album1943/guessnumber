# -*- coding: utf-8 -*-
import random

from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very hard to guess string'  # 设置secret key
bootstrap = Bootstrap(app)  # 初始化Flask-Bootstrap扩展


@app.route('/')
def index():
    # 生成一个0-1000的随机数，存储到session变量里
    session['number'] = random.randint(0, 1000)
    session['times'] = 10
    return render_template('index.html')


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    times = session['times']  # 从session变量里获取次数
    result = session.get('number')  # 从session变量里获取在index函数里生成的随机数字
    form = GuessNumberForm()
    if form.validate_on_submit():
        times -= 1
        session['times'] = times  # 更新次数值
        if times == 0:
            flash('你输啦....o(>﹏<)o')
            return redirect(url_for('.index'))
        answer = form.number.data
        if answer > result:
            flash('太大了！你还剩%s次机会！' % times)
        elif answer < result:
            flash('太小了！你还剩%s次机会！' % times)
        else:
            flash('啊哈，你赢了！V(＾－＾)V')
            return redirect(url_for('.index'))
    return render_template('guess.html', form=form)


class GuessNumberForm(Form):
    number = IntegerField('输入数字（0-1000）： ', validators=[DataRequired('输入一个有效的数字'),
                                                        NumberRange(0, 1000, '请输入0-1000内的数字！')])
    submit = SubmitField('提交')


if __name__ == '__main__':
    app.run()
