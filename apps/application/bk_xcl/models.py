# coding: utf-8
from app import db
from datetime import datetime



dbs = db.Table('dbs',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('dbconfig_id', db.Integer, db.ForeignKey('dbconfig.id'))
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120))
    role = db.Column(db.String(120))
    srole =db.Column(db.Integer, default=0)
    hash_pass = db.Column(db.String(200))
    dbs = db.relationship('Dbconfig', secondary=dbs, backref=db.backref('users', lazy='dynamic'))

    def is_authenticated(self):
        return False

    def is_active(self):
        return False

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.name)
class Dbconfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique = True )
    host = db.Column(db.String(200),)
    port = db.Column(db.Integer,default=3306)
    user = db.Column(db.String(100))
    password = db.Column(db.String(300))
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())



class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    dev = db.Column(db.String(64))
    audit = db.Column(db.String(64))
    srole = db.Column(db.Integer, default=0)
    sql_content = db.Column(db.TEXT(16777215))
    db_config = db.Column(db.String(128))
    backup = db.Column(db.Boolean, default=True)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    finish_time = db.Column(db.DateTime)
    man_review_time = db.Column(db.DateTime)
    auto_review = db.Column(db.TEXT(16777215))
    execute_result = db.Column(db.TEXT(16777215))
    timer = db.Column(db.DateTime)
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_name = db.Column(db.String(64))
    mem = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.now())
    report_content = db.Column(db.TEXT(16777215))





