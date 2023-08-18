#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import unittest

import wapp_t
import wapptpl

class TestWappTpl(unittest.TestCase):

	def test_all_export(t):
		t.assertListEqual(wapptpl.__all__, [
			'slug',
			'url',
		])

	def test_slug(t):
		t.assertEqual(wapptpl.slug('_te-st ing '), '_te_st_ing_')

	def test_url(t):
		with wapp_t.mock():
			t.assertEqual(wapptpl.url(), '/testing/')
		t.assertEqual(wapptpl.url('/'), '/')
		t.assertEqual(wapptpl.url('/testing'), '/testing')
		t.assertEqual(wapptpl.url('testing/'), 'testing/')
		t.assertEqual(wapptpl.url('testing'),  'testing')

	def test_url_args(t):
		t.assertEqual(wapptpl.url('/', 'a', 'b'), '/a/b')
		t.assertEqual(wapptpl.url('/testing', 'a', 'b'), '/testing/a/b')
		t.assertEqual(wapptpl.url('testing/', 'a', 'b'), 'testing//a/b')
		t.assertEqual(wapptpl.url('testing',  'a', 'b'), 'testing/a/b')

	def test_url_config(t):
		with wapp_t.mock(base_url = '/b'):
			t.assertEqual(wapptpl.url('/'), '/b/')
			t.assertEqual(wapptpl.url('/testing'), '/b/testing')
			t.assertEqual(wapptpl.url('testing/'), '/btesting/')
			t.assertEqual(wapptpl.url('testing'),  '/btesting')

if __name__ == '__main__':
	unittest.main()
