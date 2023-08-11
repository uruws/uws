# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import admin
import wapp

from wapptpl import url

log = wapp.getLogger(__name__)

button_class   = 'w3-button w3-border'
button_color   = 'w3-border-gray'
button_current = 'w3-border-blue w3-text-green'

input_class    = 'w3-black w3-border'
input_color    = 'w3-border-gray'

#-------------------------------------------------------------------------------
# cluster

def cluster_navbar() -> dict[str, str]:
	d: dict[str, str] = {}
	for k in admin.cluster_list():
		d[k.name] = wapp.url('/cluster/%s/' % k.name)
	return d

def cluster_info(name: str) -> admin.Cluster | None:
	try:
		return admin.cluster_info(name)
	except admin.ClusterError as err:
		log.error('%s', err)
		return None