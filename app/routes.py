from app import application
from flask import render_template, flash, redirect ,url_for
from app.forms import AnalysisForm

@application.route('/')
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

@application.route('/userPage')
def userpage_show():
    return render_template('userPage.html')