# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import admin
import wapp

log = wapp.getLogger(__name__)

#-------------------------------------------------------------------------------
# /cluster/

def index(cluster: str = ''):
	return wapp.template('admin/cluster_index.html', cluster = cluster)

#-------------------------------------------------------------------------------
# start

def start(app: wapp.Bottle):
	# /cluster/
	app.get(wapp.url('/cluster/'),           callback = index)
	app.get(wapp.url('/cluster/<cluster>/'), callback = index)
