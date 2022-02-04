# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

_outfh = sys.stdout
_errfh = sys.stderr

from contextlib import contextmanager
from os import environ, getenv, getcwd, linesep
from os import chdir as os_chdir
from pathlib import Path
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

# vendor libs
_libs = [
	'semver-2.13.0',
]
for lib in _libs:
	sys.path.insert(0, f"/srv/home/uwscli/vendor/{lib}")

import uwscli_deploy

# internal utils

def log(*args, sep = ' '):
	"""print log messages to stdout (can be disabled with UWSCLI_LOG=off env var)"""
	if _log:
		print(*args, sep = sep, file = _outfh, flush = True)

def info(*args):
	"""print log messages to stdout (even if log is disabled)"""
	print(*args, file = _outfh, flush = True)

def error(*args):
	"""print log messages to stderr"""
	print(*args, file = _errfh, flush = True)

@contextmanager
def chdir(d, error_status = 2):
	"""chdir context manager"""
	prevd = getcwd()
	dn = Path(d).expanduser()
	try:
		try:
			os_chdir(dn)
		except FileNotFoundError:
			error('[ERROR] chdir not found:', d)
			sys.exit(error_status)
		yield
	finally:
		os_chdir(prevd)

def mkdir(d, mode = 0o750, parents = True, exist_ok = True):
	"""mkdir"""
	Path(d).expanduser() \
		.mkdir(mode = mode, parents = parents, exist_ok = exist_ok)

@contextmanager
def lockf(name):
	"""lock file path"""
	p = Path(name).expanduser()
	fn = Path(p.parent, f".{p.name}.lock")
	locked = False
	try:
		fh = fn.open(mode = 'x')
		fh.close()
		locked = True
		yield fh
	finally:
		if locked:
			fn.unlink()

def _setenv(env):
	e = {}
	for k, v in environ.items():
		e[k] = v
	if env is not None:
		e.update(env)
	return e

system_ttl: int = 600

def system(cmd, env = None, timeout = system_ttl):
	"""run system commands"""
	p = proc_run(cmd, shell = True, capture_output = False,
		timeout = timeout, env = _setenv(env))
	return p.returncode

def gso(cmd):
	"""get status output from system commands"""
	return getstatusoutput(cmd)

def check_output(cmd, env = None):
	"""get output from system commands checking its exit status"""
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
	"""return list of configured apps"""
	return sorted([n for n in app.keys() if app[n].app])

def app_description():
	"""format apps list description"""
	return __desc(app_list())

def autobuild_list():
	"""return list of apps configured for autobuild"""
	return sorted([n for n in app.keys() if app[n].build and app[n].autobuild])

def autobuild_description():
	"""format apps autobuild list description"""
	return __desc(autobuild_list())

def autobuild_deploy(n: str) -> list[str]:
	"""get list of apps to deploy from an autobuild"""
	return app[n].autobuild_deploy.copy()

def build_list() -> list[str]:
	"""return list of apps configured for build"""
	return sorted([n for n in app.keys() if app[n].build.dir != ''])

def build_description():
	"""format build apps description"""
	return __desc(build_list())

def deploy_list() -> list[str]:
	"""return list of apps configured for deploy"""
	return sorted([n for n in app.keys() if app[n].deploy.image != ''])

def deploy_description():
	"""format deploy apps description"""
	return __desc(deploy_list())

def ctl(args, timeout = system_ttl):
	"""run internal app-ctl command"""
	return system("/usr/bin/sudo -H -n -u uws -- %s/app-ctl.sh %s %s" % (cmddir, _user, args),
		timeout = timeout)

def nq(cmd, args, bindir = cmddir):
	"""enqueue internal command"""
	return system("/usr/bin/sudo -H -n -u uws -- %s/uwsnq.sh %s %s/%s %s" % (cmddir, _user, bindir, cmd, args))

def run(cmd, args, cmddir: str = cmddir, timeout: int = system_ttl):
	"""run internal command"""
	return system("/usr/bin/sudo -H -n -u uws -- %s/%s %s" % (cmddir, cmd, args),
		timeout = timeout)

def clean_build(app):
	"""enqueue build clean task"""
	return system("/usr/bin/sudo -H -n -u uws -- %s/uwsnq.sh %s %s/app-clean-build.sh %s" % (cmddir, _user, cmddir, app))

# aws utils

def list_images(appname: str, region: str = '') -> list[str]:
	"""get aws ECR list of available app images"""
	kn = app[appname].cluster
	if region == '':
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

# git utils

def git_clone(rpath):
	"""git clone"""
	return system(f"git clone {rpath}")

def git_fetch(workdir = '.'):
	"""git fetch"""
	args = ''
	if workdir != '.':
		args += f" -C {workdir}"
	return system(f"git{args} fetch --prune --prune-tags --tags")

def git_checkout(tag, workdir = '.'):
	"""git checkout"""
	args = ''
	if workdir != '.':
		args += f" -C {workdir}"
	return system(f"git{args} checkout {tag}")

def git_deploy(rname, tag):
	"""run uwscli deploy"""
	return uwscli_deploy.run(rname, tag)

def git_describe(workdir = '.'):
	"""git describe"""
	args = ''
	if workdir != '.':
		args += f" -C {workdir}"
	return check_output(f"git{args} describe --always").strip()

def git_tag_list(workdir = '.'):
	"""git tag --list"""
	args = ''
	if workdir != '.':
		args += f" -C {workdir}"
	return check_output(f"git{args} tag --list").strip().split(sep = linesep)
