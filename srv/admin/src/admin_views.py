# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import wapp

import admin

log = wapp.getLogger(__name__)

#-------------------------------------------------------------------------------
# /healthz

def healthz():
	return 'ok'

#-------------------------------------------------------------------------------
# start

def start(app: wapp.Bottle):
	# /healthz
	app.get(wapp.url('/healthz'), callback = healthz)
