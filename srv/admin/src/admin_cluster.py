# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import admin
import wapp

log = wapp.getLogger(__name__)

#-------------------------------------------------------------------------------
# /cluster/

def index(name: str = ''):
	name = name.strip()
	try:
		admin.cluster_info(name)
	except admin.ClusterError as err:
		return wapp.error(404, 'admin/cluster_index.html', admin_cluster = name, has_error = True)
	return wapp.template('admin/cluster_index.html', admin_cluster = name, has_error = False)

#-------------------------------------------------------------------------------
# start

def start(app: wapp.Bottle):
	# /cluster/
	app.get(wapp.url('/cluster/'),        callback = index)
	app.get(wapp.url('/cluster/<name>/'), callback = index)
