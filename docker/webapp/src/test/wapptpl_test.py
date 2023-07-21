#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import wapp_t
import wapptpl

class TestWappTpl(unittest.TestCase):

	def test_all_export(t):
		t.assertListEqual(wapptpl.__all__, [
			'url',
		])

	def test_url(t):
		t.assertEqual(wapptpl.url('/testing'), '/testing')
		t.assertEqual(wapptpl.url('testing/'), 'testing/')
		t.assertEqual(wapptpl.url('testing'),  'testing')

	def test_url_args(t):
		t.assertEqual(wapptpl.url('/testing', 'a', 'b'), '/testing/a/b')
		t.assertEqual(wapptpl.url('testing/', 'a', 'b'), 'testing//a/b')
		t.assertEqual(wapptpl.url('testing',  'a', 'b'), 'testing/a/b')

	def test_url_config(t):
		with wapp_t.mock(base_url = '/b'):
			t.assertEqual(wapptpl.url('/testing'), '/b/testing')
			t.assertEqual(wapptpl.url('testing/'), '/btesting/')
			t.assertEqual(wapptpl.url('testing'),  '/btesting')

if __name__ == '__main__':
	unittest.main()
