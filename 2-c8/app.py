import os
import json
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

client = MongoClient('127.0.0.1',27017)
mgdb = client.shiyanlou

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
    def add_tag(self,tag_name):
        tag = mgdb.tag.find_one({'fileid':self.id})
        if tag is None:
            tag_list = []
            tag_list.append(tag_name)
            tag = {'fileid':self.id,'tags':tag_list}
            mgdb.tag.insert_one(tag)
        else:
            tag_list = tag['tags']
            if tag_name not in tag_list:
                tag_list.append(tag_name)
                mgdb.tag.update_one({'fileid':self.id},{'$set':{'tags':tag_list}})
    def remove_tag(self,tag_name):
        tag = mgdb.tag.find_one({'fileid':self.id})
        tag_list = tag['tags']
        if tag is not None and tag_name in tag_list:
            tag_list.remove(tag_name)
            mgdb.tag.update_one({'fileid':self.id},{'$set':{'tags':tag_list}})
    @property
    def tags(self):
        return mgdb.tag.find_one({'fileid':self.id})['tags']



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
    file_list = []
    for f in files:
        dict_file = {}
        dict_file['title']=f.title
        dict_file['path']='/files/'+str(f.id)
        dict_file['tags']=','.join(mgdb.tag.find_one({'fileid':f.id})['tags'])
        file_list.append(dict_file)
    return render_template('index.html',file_list=file_list)

@app.route('/files/<file_id>')
def file(file_id): 
    file_ids = [str(f.id) for f in db.session.query(File).all()]
    if file_id not in file_ids:
        abort(404)
    else:
        ff = db.session.query(File).filter(File.id==int(file_id)).one()
    return render_template('file.html',ff=ff)
