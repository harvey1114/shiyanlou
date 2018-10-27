import os
import json
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True

@app.errorhandler(404)
def not_fount(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    dir_path = '/home/shiyanlou/files'
    filelist = []
    for filename in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path,filename)):
            filelist.append(filename.split('.')[0])
    if 'helloshiyanlou' not in filelist or 'helloworld' not in filelist:
        abort(404)

    return render_template('index.html',filelist=filelist)

@app.route('/files/<filename>')
def file(filename):
    filepath = os.path.join('/home/shiyanlou/files',filename+'.json')
    with open(filepath,'r')as f:
        filecontent = json.load(f)
        print(filecontent)
    return render_template('file.html',filecontent=filecontent)
