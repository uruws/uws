# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import wapp

import admin
import admin_app
import admin_cluster

log = wapp.getLogger(__name__)

#-------------------------------------------------------------------------------
# /healthz

def healthz():
	return wapp.text_plain('ok')

#-------------------------------------------------------------------------------
# /

def home():
	# ~ return wapp.template('admin/home.html')
	return wapp.redirect(wapp.url('/cluster/'))

#-------------------------------------------------------------------------------
# start

def start(app: wapp.Bottle):
	# /healthz
	app.get(wapp.url('/healthz'), callback = healthz)
	# /cluster/
	admin_cluster.start(app)
	# /app/
	admin_app.start(app)
	# /
	app.get(wapp.url('/'), callback = home)
