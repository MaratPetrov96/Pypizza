from app import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db=SQLAlchemy(app)

migrate = Migrate(app, db)

table=db.Table('table', #таблица для связи заказчика и меню
    db.Column('food_id',db.Integer,db.ForeignKey('food.id')),
    db.Column('user_id',db.Integer,db.ForeignKey('visitor.id'))
               )

table2=db.Table('table2', #таблица для связи заказа и меню
    db.Column('food_id',db.Integer,db.ForeignKey('food.id')),
    db.Column('order_id',db.Integer,db.ForeignKey('order.id'))
    )

class User(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True,nullable=False)
    name=db.Column(db.String(16),nullable=False)
    password=db.Column(db.String(200),nullable=False)

class Kind(db.Model): #раздел меню
    id=db.Column(db.Integer, primary_key=True,nullable=False)
    name=db.Column(db.String(20),nullable=False)

class Food(db.Model):
    id=db.Column(db.Integer, primary_key=True,nullable=False)
    kind_id=db.Column(db.Integer, db.ForeignKey('kind.id'),nullable=False)
    name=db.Column(db.String(100),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    description=db.Column(db.Text)
    picture=db.Column(db.String(),nullable=False)
    def __repr__(self):
        return self.name

class Visitor(db.Model): #клиент
    id=db.Column(db.Integer, primary_key=True,nullable=False)
    ip=db.Column(db.String(20),nullable=False)
    order=db.relationship('Food',backref=db.backref(
        'buyers',lazy=True),lazy='dynamic',secondary=table)

class Order(db.Model): #заказ
    id=db.Column(db.Integer, primary_key=True,nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    products=db.relationship('Food',backref=db.backref(
        'orders',lazy=True),lazy='dynamic',secondary=table2)
    s=db.Column(db.Integer)

db.create_all()
