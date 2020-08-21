from flask import Flask,jsonify
from flask_socketio import SocketIO
application=Flask(__name__,template_folder='app/templates')
socketio = SocketIO(application)
from flask import render_template,request
import pika
import os
from pymongo import MongoClient


@application.route('/')
def healthcheck():
    return render_template('/tracer.html')

@application.route('/put',methods=['GET'])
def put():
    credentials = pika.PlainCredentials('testuser', 'pass')   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host'),credentials=credentials,heartbeat=120))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('sender_queue'), durable=True)
    channel.basic_publish(body='up', exchange='',routing_key=os.environ.get('sender_queue'))
    channel.close()
    return "done"

@application.route('/soc',methods=['POST'])
def update():
    input_json = request.get_json(force=True)
    socketio.emit('event',{'data': input_json},namespace='/test')
    return render_template('demo.html')

@application.route('/logs/<string:entity>',methods=['GET'])
def logs(entity):
    logs_obj=(mongo[entity]).find()
    logs=[]
    for i in logs_obj:
        logs.append(i)
    return render_template('logs.html',data=logs)

if __name__ == '__main__':
    #os.environ['mongo_addr'] = '192.168.99.100'
    mongo = 'mongodb://' + os.environ['mongo_addr'] + ':27017/'
    client = MongoClient(mongo)
    mongo = client["logs"]
    #os.environ['mq_host']='192.168.99.100'
    socketio.run(application,host="0.0.0.0")
