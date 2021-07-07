from flask import Flask,render_template,redirect,request,abort,flash,url_for
from flask_mail import Mail,Message
from flask_login import LoginManager,login_user,current_user,login_required,UserMixin,logout_user

app=Flask(__name__,static_folder='food')

app.config['UPLOAD_FOLDER']='food'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///food.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['SECRET_KEY'] = 'secret key'

app.config.update(
MAIL_SERVER = 'smtp.googlemail.com',
MAIL_PORT = 465,
MAIL_USE_TLS = False,
MAIL_USE_SSL = True,
MAIL_USERNAME = 'pypizza',
MAIL_PASSWORD = 'password')

admin_mail=['pypizza@gmail.com']

mail=Mail(app)
