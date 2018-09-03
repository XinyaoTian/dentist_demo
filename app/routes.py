# -*- encoding:utf-8 -*-
from app import application
from flask import render_template, flash, redirect ,url_for ,request
from app.forms import AnalysisForm
import logging
logging.basicConfig(level=logging.INFO)

@application.route('/index')
@application.route('/welcomePage')
def index():
    user = {'username':'Doctor'}
    posts = [
        {
            'author' : {'username' : 'John'},
            'body' : 'Good day today!'
        },
        {
            'author' : {'username' : 'Susan'},
            'body' : "Let's start analysing!"
        }
    ]
    return render_template('welcomePage.html', title = 'FrontPage', user = user , posts = posts)

@application.route('/input', methods=['Get','POST'])
def analysis():
    form = AnalysisForm()
    if form.validate_on_submit():
        flash('Data need to be analysed x1 = {}, x2 = {}'.format(
            form.x1.data,form.x2.data))
        return redirect(url_for('welcomePage'))
    return render_template('input.html', title="Let's start analysis!", form=form)

@application.route('/result')
def show_result():
    posts = {
        'X1':12,
        'X2':2,
        'Y':12.2
    }
    return render_template('result.html',title="Results", posts = posts)

@application.route('/')
@application.route('/userPage')
def userpage_show():
    return render_template('userPage.html')

@application.route('/inputPage')
def inputpage_show():
    return render_template('inputPage.html')

@application.route('/analysisPage')
def analysispage_show():
    post = {'patientId': u'未知', 'description': u'未输入任何病人数据，无法分析!'}
    return render_template('analysisPage.html', post = post)

@application.route('/analysisPage', methods=['Get','POST'])
def analysispage_parse():
    if request.form['patientId'] is not None:
        patientId = request.form['patientId']
        post = {'patientId':patientId ,'description':u'根据病人的各项指标，机器学习模型预测诊断如下:'}
        logging.info(str(post['patientId']))
        return render_template('analysisPage.html' , post = post)
    else:
        post = {'patientId':u'未知' , 'description':u'未输入任何病人数据，无法分析!'}
        return render_template('analysisPage.html', post=post )

@application.route('/tutorialPage')
def tutorialpage_show():
    return render_template('tutorialPage.html')