from flask import Blueprint,render_template,request,url_for,redirect
# trace_bp = Blueprint('trace_bp',__name__, template_folder='templates', url_prefix='/trace')
# from flask_socketio import emit
#
# @trace_bp.route('/')
# def healthcheck():
#     #host=os.env
#     #socketio.emit('event',{})
#     return render_template('tracer.html')
#
#
# @trace_bp.route('/soc')
# def healthcheck1():
#     #host=os.env
#     emit('event',
#          {'data': 2, 'count': 1})
#     #emit('event',{'data': 1},namespace='http://127.0.0.1:5000/test', broadcast=True)
#     return render_template('tracer.html')
#
# # @socketio.on('my_event', namespace='/test')
# # def test_message(message):
# #     emit('my_response',
# #          {'data': message['data'], 'count': 1})
