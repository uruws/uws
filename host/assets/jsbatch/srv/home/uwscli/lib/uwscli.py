# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

_outfh = sys.stdout
_errfh = sys.stderr

from os import getenv
from os import chdir as os_chdir
from os import system as os_system
from subprocess import getstatusoutput, CalledProcessError
from subprocess import check_output as proc_check_output

_user = getenv('USER', 'unknown')
_log = getenv('UWSCLI_LOG', 'on') == 'on'

from uwscli_conf import app, cluster, bindir, cmddir, docker_storage, docker_storage_min

def chdir(d):
	os_chdir(d)

def system(cmd):
	return os_system(cmd) >> 8

def gso(cmd):
	return getstatusoutput(cmd)

def check_output(cmd, shell = True):
	return proc_check_output(cmd, shell = shell).decode('utf-8')

def log(*args, sep = ' '):
	if _log:
		print(*args, sep = sep, file = _outfh)

def error(*args):
	print(*args, file = _errfh)

def __descmax(k):
	m = 0
	for s in k:
		l = len(s)
		if l > m:
			m = l
	return m

def __descsep(k, m):
	s = ' '
	for i in range(len(k), m):
		s += ' '
	return s

def __desc(apps):
	m = __descmax(apps)
	d = 'available apps:\n'
	for n in apps:
		d += "  %s%s- %s\n" % (n, __descsep(n, m), app[n].desc)
	return d

def app_list():
	return sorted([n for n in app.keys() if app[n].app])

def app_description():
	return __desc(app_list())

def build_list():
	return sorted([n for n in app.keys() if app[n].build is not None])

def build_description():
	return __desc(build_list())

def deploy_list():
	return sorted([n for n in app.keys() if app[n].deploy is not None])

def deploy_description():
	return __desc(deploy_list())

def ctl(args):
	return system("/usr/bin/sudo -H -n -u uws -- %s/app-ctl.sh %s %s" % (cmddir, _user, args))

def nq(cmd, args, build_dir = cmddir):
	return system("/usr/bin/sudo -H -n -u uws -- %s/uwsnq.sh %s %s/%s %s" % (cmddir, _user, build_dir, cmd, args))

def run(cmd, args):
	return system("/usr/bin/sudo -H -n -u uws -- %s/%s %s" % (cmddir, cmd, args))

def clean_build(app, version):
	return system("/usr/bin/sudo -H -n -u uws -- %s/uwsnq.sh %s %s/app-clean-build.sh %s %s" % (cmddir, _user, cmddir, app, version))

def list_images(appname, region = None):
	kn = app[appname].cluster
	if region is None:
		region = cluster[kn]['region']
	cmd = "aws ecr list-images --output text --repository-name uws"
	cmd += " --region %s" % region
	cmd += " | grep -F '%s'" % app[appname].deploy.image
	cmd += " | awk '{ print $3 }'"
	cmd += " | sed 's/^%s//'" % app[appname].deploy.filter
	cmd += " | sort -n"
	try:
		out = check_output(cmd)
		return out.splitlines()
	except CalledProcessError as err:
		error(f"[ERROR] {appname} list images: {err.output}")
	return []
