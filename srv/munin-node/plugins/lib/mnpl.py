# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import json

from dataclasses import dataclass
from dataclasses import field
from os          import getenv
from pathlib     import Path
from time        import time

from http.client  import HTTPResponse
from urllib.error import HTTPError

from typing import Union

import mnpl_utils as utils

#
# clusters config
#

_clusters_fn     = Path(getenv('UWS_CLUSTER_ENV', '/uws/etc/cluster.json'))
_clusters_domain = getenv('UWS_CLUSTER_DOMAIN', 'uws.talkingpts.org')

def clusters() -> list[dict[str, str]]:
	"""Returns clusters info."""
	k: list[dict[str, str]] = []
	with open(_clusters_fn, 'r') as fh:
		k = [d for d in json.load(fh) if d]
	return k

#
# plugin config
#

@dataclass
class Config(object):
	domain:             str = _clusters_domain
	auth:              bool = True
	path:               str = '/'
	status:             int = 200
	status_valid: list[int] = field(default_factory = list)
	timeout:            int = 15
	category:           str = ''
	label:              str = 'number'
	title:              str = ''
	base:               int = 1000
	scale:             bool = True
	warning:            int = 13
	critical:           int = 15

@dataclass
class HostConfig(object):
	name: str = ''
	host: str = ''

#
# http helpers
#

def GET(cluster: str, cfg: Config) -> HTTPResponse:
	url = f"https://{cluster}.{cfg.domain}{cfg.path}"
	return utils.GET(url, timeout = cfg.timeout, auth = cfg.auth)

#
# config
#

def config_host(h: HostConfig, cfg: Config) -> int:
	gid  = utils.cleanfn(f"{h.name}_{cfg.path}_{cfg.status}")
	title = cfg.path
	if not cfg.auth:
		title += ' (no auth)'
		gid += '_no_auth'
	utils.println(f"multigraph k8s_{gid}")
	if cfg.title != '':
		utils.println(f"graph_title k8s {h.name} {cfg.title}")
	else:
		utils.println(f"graph_title k8s {h.name} {title}")
	utils.println(f"graph_args --base {cfg.base} -l 0")
	if cfg.category != '':
		utils.println('graph_category', cfg.category)
	else:
		utils.println('graph_category', utils.cleanfn(h.name))
	utils.println('graph_vlabel', cfg.label)
	if cfg.scale:
		utils.println('graph_scale yes')
	utils.println('a_latency.label latency seconds')
	utils.println('a_latency.colour COLOUR0')
	utils.println('a_latency.draw AREA')
	utils.println('a_latency.min 0')
	utils.println('a_latency.warning', cfg.warning)
	utils.println('a_latency.critical', cfg.critical)
	utils.println('a_latency.info', f"https://{h.host}.{cfg.domain}{cfg.path}")
	utils.println('b_status.label status:', cfg.status)
	utils.println('b_status.colour COLOUR1')
	utils.println('b_status.draw LINE')
	utils.println('b_status.min 0')
	utils.println('b_status.max 1')
	utils.println('b_status.critical 1:')
	return 0

def config(cfg: Config) -> int:
	rc = 0
	for k in clusters():
		h = HostConfig(
			name = k['name'],
			host = k['host'],
		)
		st = config_host(h, cfg)
		if st != 0: rc += 1
	return rc

#
# report
#

def _report(host: str, cfg: Config) -> tuple[float, float]:
	t: float = time()
	s: float = 0.0
	r: Union[HTTPResponse, HTTPError, None] = None
	try:
		r = GET(host, cfg)
	except HTTPError as err:
		r = err
	if r is not None:
		code: int | None = r.getcode()
		if code is not None:
			if code == cfg.status or code in cfg.status_valid:
				s = 1.0
	return (s, time() - t)

def report_host(h: HostConfig, cfg: Config) -> int:
	gid  = utils.cleanfn(f"{h.name}_{cfg.path}_{cfg.status}")
	if not cfg.auth:
		gid += '_no_auth'
	utils.println(f"multigraph k8s_{gid}")
	st = ''
	lt = ''
	try:
		status, latency = _report(h.host, cfg)
		st = str(status)
		lt = str(latency)
	except Exception as err:
		utils.error(err)
		st = 'U'
		lt = 'U'
	utils.println('a_latency.value', lt)
	utils.println('b_status.value', st)
	return 0

def report(cfg: Config) -> int:
	rc = 0
	for k in clusters():
		h = HostConfig(
			name = k['name'],
			host = k['host'],
		)
		st = report_host(h, cfg)
		if st != 0: rc += 1
	return rc

#
# main
#

def main(argv: list[str], cfg: Config) -> int:
	try:
		action = argv[0]
	except IndexError:
		action = 'report'
	if action == 'config':
		return config(cfg)
	return report(cfg)
