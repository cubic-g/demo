#!/usr/bin/env python

import os

from flask import Flask, send_file, jsonify

from config import config

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

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

	return app
