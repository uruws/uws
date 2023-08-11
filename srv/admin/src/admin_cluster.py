# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import wapp

log = wapp.getLogger(__name__)

#-------------------------------------------------------------------------------
# /cluster/

def index():
	return wapp.template('admin/cluster_index.html')

#-------------------------------------------------------------------------------
# start

def start(app: wapp.Bottle):
	# /cluster/
	app.get(wapp.url('/cluster/'), callback = index)
