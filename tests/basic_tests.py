#!/usr/bin/env python

import unittest

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
		url = url_for('whoami')
		rv = self.client.open(url, method='GET')
		testcase.assertInInstance(rv, dict)
		testcase.assertTrue('message' in rv)
		testcase.assertIsInstance(rv['message'], basestring)
