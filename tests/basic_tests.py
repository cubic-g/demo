#!/usr/bin/env python

import unittest
import json

from flask import url_for

from app import create_app

class MyTestCase(unittest.TestCase):

	def setUp(self):
		self.app = app = create_app('testing')
		self.client = app.test_client()

	def tearDown(self):
		pass

	def test_whoami(self):
		testcase = self
		with self.app.test_request_context():
			url = url_for('whoami')
		rv = self.client.open(url, method='GET')
		data = rv.get_data()
		testcase.assertEqual(rv.mimetype, 'application/json')
		testcase.assertEqual(rv.status_code, 200)
		data = json.loads(data)
		testcase.assertIsInstance(data, dict)
		testcase.assertTrue('message' in data)
		testcase.assertIsInstance(data['message'], basestring)
