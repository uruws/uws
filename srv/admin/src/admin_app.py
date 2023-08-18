# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import admin
import wapp

log = wapp.getLogger(__name__)

#-------------------------------------------------------------------------------
# /app/

def index(name: str = ''):
	name = name.strip()
	if name != '':
		try:
			admin.app_info(name)
		except admin.AppError as err:
			return wapp.error(404, 'admin/app_index.html', admin_app = name)
	return wapp.template('admin/app_index.html', admin_app = name)

#-------------------------------------------------------------------------------
# start

def start(app: wapp.Bottle):
	# /app/
	app.get(wapp.url('/app/'),        callback = index)
	app.get(wapp.url('/app/<name>/'), callback = index)
