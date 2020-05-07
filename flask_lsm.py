from gevent import monkey
import json,io
from gevent import pywsgi
from multiprocessing import cpu_count, Process
from flask import Flask,request
from yolo import *
import luosimao

yolo = YOLO()
app = Flask(__name__)
@app.route("/api/",methods=['POST'])
def index():
    try:
        site_keys = request.json
        site_key=site_keys['site_key']
        print(site_key)
        if len(site_key) == 32:
            rep = luosimao.run(yolo,site_key)
        else:
            rep = {'code':'400','msg':'input paras error'}
        return json.dumps(rep)
    except:
        print('调用失败')

@app.route("/api/",methods=['GET'])
def hello():
    try:
        site_key = request.args.get('site_key')
        if len(site_key) == 32:
            rep = luosimao.run(yolo,site_key)
        else:
            rep = {'code':'400','msg':'input paras error'}
        return json.dumps(rep)
    except:
        print('调用失败')
server = pywsgi.WSGIServer(('192.168.8.199', 7781), app)
server.serve_forever()

