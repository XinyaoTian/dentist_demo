from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me = BooleanField("Remeber Me")
    submit = SubmitField("Sign In")

class AnalysisForm(FlaskForm):
    x1 = StringField("X1",validators=[DataRequired()])
    x2 = StringField("X2", validators=[DataRequired()])
    x3 = StringField("X3", validators=[DataRequired()])
    x4 = StringField("X4", validators=[DataRequired()])
    x5 = StringField("X5", validators=[DataRequired()])
    x6 = StringField("X6", validators=[DataRequired()])
    x7 = StringField("X7", validators=[DataRequired()])
    x8 = StringField("X8", validators=[DataRequired()])
    x9 = StringField("X9", validators=[DataRequired()])
    x10 = StringField("X10", validators=[DataRequired()])
    x11 = StringField("X11", validators=[DataRequired()])
    submit = SubmitField("Start Analysis")