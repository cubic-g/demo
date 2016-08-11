#!/usr/bin/env python

import unittest
import json
import re
from functools import wraps, partial

from flask import url_for

from app import create_app


def check_result(testcase, spec, result):
	if spec is None:
		return
	elif isinstance(spec, type):
		testcase.assertIsInstance(result, spec,
			'expecting {0}, got {1}'.format(spec.__name__, type(result)))
	elif isinstance(spec, dict):
		testcase.assertIsInstance(result, dict,
			'expecting a dict, got {0}'.format(repr(result)))
		for key, child_spec in spec.iteritems():
			testcase.assertIn(key, result,
				'key {0} not found in {1}'.format(key, result))
			value = result[key]
			check_result(testcase, child_spec, value)
	elif isinstance(spec, set):
		testcase.assertIsInstance(result, dict,
			'expecting a dict, got {0}'.format(repr(result)))
		for key in spec:
			if isinstance(key, basestring):
				testcase.assertIn(key, result,
					'key {0} not found in {1}'.format(key, result))
			elif isinstance(key, tuple):
				key, child_spec = key
				testcase.assertIn(key, result,
					'key {0} not found in {1}'.format(key, result))
				value = result[key]
				check_result(testcase, child_spec, value)
	elif isinstance(spec, tuple):
		testcase.assertIsInstance(result, list,
			'expecting a list, got {0}'.format(repr(result)))
		length = len(result)
		length_expression, member_spec = spec
		match = re.match('(?P<op><|<=|==|>|>=)(?P<value>\d+)$', length_expression)
		if not match:
			testcase.fail('unable to verify result list length: {0}'.format(length_expression))
		op = match.group('op')
		v = int(match.group('value'))
		if op == '<':
			testcase.assertLess(length, v)
		elif op == '<=':
			testcase.assertLessEqual(length, v)
		elif op == '==':
			testcase.assertEqual(length, v)
		elif op == '>':
			testcase.assertGreater(length, v)
		else:
			testcase.assertGreaterEqual(length, v)
		if length:
			first = result[0]
			check_result(testcase, member_spec, first)


def run_test(method='GET', headers=None, data=None,
	content_type='application/json', expected_mimetype='application/json',
	expected_status_code=200, expected_result=None, environ_overrides={},
	**values):
	if method not in ('GET', 'PATCH', 'POST', 'HEAD', 'PUT',
			'DELETE', 'OPTIONS', 'TRACE'):
		raise ValueError, 'invalid method'
	request_data = json.dumps(data) if content_type == 'application/json' else data
	def testcase_injection_decorator(fn):
		@wraps(fn)
		def testcase_injected(*args, **kwargs):
			testcase = self = args[0]
			try:
				# return value is ignored
				fn(*args, **kwargs)
			except NotImplementedError, e:
				# implemented now
				pass

			headers = {}
			headers.update(getattr(testcase, 'headers', {}))
			with self.app.test_request_context():
				name = fn.__name__[5:].replace('__', '.')
				url = url_for(name, **values)
			rv = self.client.open(url, method=method,
				environ_overrides=environ_overrides,
				headers=headers,
				content_type=content_type, data=request_data)
			testcase.assertEqual(rv.mimetype, expected_mimetype,
				'expected mimetype {0}, got {1}'.format(expected_mimetype, rv.mimetype))
			testcase.assertEqual(rv.status_code, expected_status_code,
				'expected status code {0}, got {1}\n{2}'.format(expected_status_code, rv.status_code, rv.get_data()))
			if expected_result is None:
				return
			if expected_mimetype == 'application/json':
				data = json.loads(rv.get_data())
				testcase.assertIsInstance(data, dict)
				# check result recursively
				check_result(self, expected_result, data)
		return testcase_injected
	return testcase_injection_decorator


for _ in ('put', 'post', 'delete', 'get'):
	locals()[_] = partial(run_test, method=_.upper())


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

	@get(expected_result={'users': ('==2', {'userId', 'email', 'familyName', 'givenName'})})
	def test_api_1_0__get_users(self):
		raise NotImplementedError

	@get(expected_result={'addresses': ('==4', {'addressId', 'street0', 'street1', 'city', 'province'})})
	def test_api_1_0__get_addresses(self):
		raise NotImplementedError
