import os
import json
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category')
    content = db.Column(db.Text)
    def __init__(self,title,created_time,category,content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File:{}>'.format(self.title)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    def __init__(self,name):
        self.name = name
    def __repr__(self):
        return '<Category:{}>'.format(self.name)

@app.errorhandler(404)
def not_fount(error):
    return render_template('404.html'), 404


@app.route('/')
def index(): 
    files = db.session.query(File).all()
    dict_file = {}
    for f in files:
        dict_file[f.title]='/files/'+str(f.id)
    print(dict_file)
    return render_template('index.html',dict_file=dict_file)

@app.route('/files/<file_id>')
def file(file_id): 
    file_ids = [str(f.id) for f in db.session.query(File).all()]
    if file_id not in file_ids:
        abort(404)
    else:
        ff = db.session.query(File).filter(File.id==int(file_id)).one()
    return render_template('file.html',ff=ff)
