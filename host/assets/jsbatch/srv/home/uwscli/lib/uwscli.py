# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

_outfh = sys.stdout
_errfh = sys.stderr

from contextlib import contextmanager
from os import environ, getenv, getcwd
from os import chdir as os_chdir
from subprocess import getstatusoutput, CalledProcessError
from subprocess import check_output as proc_check_output
from subprocess import run as proc_run

_user = getenv('USER', 'unknown')
_log = getenv('UWSCLI_LOG', 'on') == 'on'

_env = {
	'PATH': '/srv/home/uwscli/bin:/usr/local/bin:/usr/bin:/bin',
}
environ.update(_env)

from uwscli_conf import app, cluster, bindir, cmddir, docker_storage, docker_storage_min

import uwscli_deploy

def log(*args, sep = ' '):
	if _log:
		print(*args, sep = sep, file = _outfh)

def error(*args):
	print(*args, file = _errfh)

@contextmanager
def chdir(d, error_status = 2):
	prevd = getcwd()
	try:
		try:
			os_chdir(d)
		except FileNotFoundError:
			error('[ERROR] chdir not found:', d)
			sys.exit(error_status)
		yield
	finally:
		os_chdir(prevd)

_cmdTtl = 180

def _setenv(env):
	e = {}
	for k, v in environ.items():
		e[k] = v
	if env is not None:
		e.update(env)
	return e

def system(cmd, env = None, timeout = _cmdTtl):
	p = proc_run(cmd, shell = True, capture_output = True,
		timeout = timeout, env = _setenv(env))
	return p.returncode

def gso(cmd):
	return getstatusoutput(cmd)

def check_output(cmd, env = None):
	return proc_check_output(cmd, shell = True, env = _setenv(env)).decode('utf-8')

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

def git_clone(rpath):
	return system(f"git clone {rpath}")

def git_fetch():
	return system("git fetch --prune --prune-tags --tags")

def git_checkout(tag):
	return system(f"git checkout {tag}")

def git_deploy(rname, tag):
	return uwscli_deploy.run(rname, tag)
