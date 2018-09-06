# -*- encoding:utf-8 -*-
from app import application
from flask import render_template, flash, redirect ,url_for ,request
from app.forms import AnalysisForm
from app.FunctionalModels.PredictionAnalysis import PredictionAnalysis
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
    # 临时代码----
    post_data = {
        'Y_probability_lr': 0,
        'Y_probability_rfc': 0,
        'Y_probability_gbtc': 0,
        'Y_probability_svc': 0 ,
        'Y_prediction_svc': 0,
        'Y_prediction_gbtreg': 0,
        'Y_prediction_gbtc': 0,
        'isAvailable':u'无数据'
    }
    # 临时代码结束----
    return render_template('analysisPage.html', post = post ,post_data = post_data)

@application.route('/analysisPage', methods=['Get','POST'])
def analysispage_parse():
    if request.form['patientId'] is not None:
        try:
            patientId = request.form['patientId']

            X1 =float(request.form['X1'])
            X2 = float(request.form['X2'])
            X3 = float(request.form['X3'])
            X4 = float(request.form['X4'])
            X5 = float(request.form['X5'])
            X6 = float(request.form['X6'])
            X7 = float(request.form['X7'])
            X8 = float(request.form['X8'])
            X9 = float(request.form['X9'])
            X10 = float(request.form['X10'])
            X11 = float(request.form['X11'])

            param_dict = {
                'X1':X1, 'X2':X2, 'X3':X3, 'X4':X4, 'X5':X5, 'X6':X6,
                'X7':X7, 'X8':X8, 'X9':X9, 'X10':X10, 'X11':X11
                          }
            logging.info(str(param_dict))
        except:
            flash(u"输入信息存在不正确格式。请注意: 各项指标只能为数字; 各项指标均不能为空值。")
            return render_template('inputPage.html')
        post = {'patientId':patientId ,'description':u'根据病人的各项指标，机器学习模型预测诊断如下:'}

        # 机器学习代码
        pa = PredictionAnalysis()
        post_data = pa.analysisData_webOutput(param_dict)
        if post_data['Y_prediction_gbtc'] >= 1.0:
            post_data['isAvailable'] = u"治疗有效"
        else:
            post_data['isAvailable'] = u"治疗无效"
        # 机器学习代码结束

        # # 临时代码----
        # post_data = {
        #     'Y_probability_lr': 82,
        #     'Y_probability_rfc': 79,
        #     'Y_probability_gbtc': 94,
        #     'Y_probability_svc': 98,
        #     'Y_prediction_gbtreg': 3.2,
        #     'Y_prediction_gbtc': 1.0
        # }
        #
        # if post_data['Y_prediction_gbtc'] >= 1.0:
        #     post_data['isAvailable'] = u"治疗有效"
        # else:
        #     post_data['isAvailable'] = u"治疗无效"
        # # 临时代码结束----
        return render_template('analysisPage.html' , post = post,post_data = post_data , param_dict = param_dict)
    else:
        pass
        # 因为即使病人的id输入的是空值，request.form['patientId'] 也不会为 None 因此分支几乎无效
        # post = {'patientId':u'未知' , 'description':u'未输入任何病人数据，无法分析!'}
        # return render_template('analysisPage.html', post=post )

@application.route('/tutorialPage')
def tutorialpage_show():
    return render_template('tutorialPage.html')

@application.route('/waitingPage')
def waitingpage_show():
    return render_template('waitingPage.html')