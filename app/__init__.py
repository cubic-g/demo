#!/usr/bin/env python

import os

from flask import Flask, send_file, jsonify, request, session, redirect

from config import config
import db.model as m
from db.db import SS
from db import database as db
from .auth import MyAuthMiddleWare
from .i18n import get_text as _

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	db.init_app(app)

	# app.wsgi_app = MyAuthMiddleWare(app.wsgi_app,
	# 	app.config['AUTHENTICATION_LOGIN_URL'],
	# 	public_prefixes=['/static/', '/favicon.ico', '/logout'],
	# 	json_prefixes=['/api/'],
	# )

	from app.api import api_1_0
	app.register_blueprint(api_1_0, url_prefix='/api/1.0/')

	@app.before_request
	def get_current_user():
		data = request.environ.get('myauthmiddleware', None)
		if data and data['REMOTE_USER_ID']:
			user = m.User.query.get(data['REMOTE_USER_ID'])
		else:
			user = m.User.query.get(1)
		session['current_user'] = user

	@app.after_request
	def clear_current_user(resp):
		session['current_user'] = None
		return resp

	@app.teardown_request
	def terminate_transaction(exception):
		if exception is None:
			SS.commit()
		else:
			SS.rollback()
		SS.remove()

	@app.route('/')
	def index():
		return send_file(os.path.join(os.path.dirname(__file__), 'index.html'))

	@app.route('/favicon.ico')
	def favicon():
		return send_file(os.path.join(os.path.dirname(__file__), 'favicon.ico'))

	@app.route('/whoami')
	def whoami():
		return jsonify(message=os.environ.get('AWS_ENV', 'unknown'))

	@app.route('/hello')
	def hello():
		return jsonify(message='hello, world.')

	@app.errorhandler(404)
	def default_hander(exc):
		if request.path.startswith('/static'):
			return make_response(
				_('Sorry, the resource you have requested for is not found'),
				404)
		# TODO: only redirect valid urls
		return redirect('/#%s' % request.path)

	return app
