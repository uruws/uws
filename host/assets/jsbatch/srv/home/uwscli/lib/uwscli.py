# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import re
import sys

from typing     import Optional
from contextlib import contextmanager

from os import environ, getcwd, linesep
from os import chdir as os_chdir

from pathlib    import Path
from subprocess import PIPE
from subprocess import getstatusoutput, CalledProcessError
from subprocess import check_output as proc_check_output
from subprocess import run as proc_run
from uuid       import uuid5
from uuid       import NAMESPACE_DNS

from uwscli_auth import User, getuser, user_auth

_user: User = getuser()

_env: dict[str, str] = {
	'PATH': '/srv/home/uwscli/bin:/usr/local/bin:/usr/bin:/bin',
}
environ.update(_env)

from uwscli_conf import app, cluster, bindir, cmddir
from uwscli_conf import docker_storage, docker_storage_min

def _local_conf(cfgdir: str = '/etc/uws/cli'):
	if Path(cfgdir).is_dir():
		fn = Path(cfgdir, 'local_conf.py')
		if fn.is_file() and not fn.is_symlink():
			sys.path.insert(0, cfgdir)
			import local_conf # type: ignore
_local_conf()

#
# vendor libs
#

_libs: list[str] = [
	'semver-2.13.0',
]
for lib in _libs:
	sys.path.insert(0, f"/srv/home/uwscli/vendor/{lib}")

#
# internal utils
#

import uwscli_deploy

from uwscli_log import log, info, debug, error

from uwscli_version import VERSION

def version() -> str:
	return f"uwscli version {VERSION}"

@contextmanager
def chdir(d: str, error_status: int = 2):
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

def mkdir(d: str, mode: int = 0o750, parents: bool = True, exist_ok: bool = True):
	"""mkdir"""
	Path(d).expanduser() \
		.mkdir(mode = mode, parents = parents, exist_ok = exist_ok)

@contextmanager
def lockf(name: str):
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

#
# system utils
#

def _setenv(env: Optional[dict[str, str]]) -> dict[str, str]:
	e = {}
	for k, v in environ.items():
		e[k] = v
	if env is not None:
		e.update(env)
	return e

system_ttl: int = 600

def system(cmd: str, env: dict[str, str] | None = None, timeout: int = system_ttl) -> int:
	"""run system commands"""
	p = proc_run(cmd, shell = True, capture_output = False, timeout = timeout,
		stdout = None, stderr = None, env = _setenv(env))
	return p.returncode

def gso(cmd: str) -> tuple[int, str]:
	"""get status output from system commands"""
	return getstatusoutput(cmd)

def check_output(cmd: str, env: dict[str, str] | None = None) -> str:
	"""get output from system commands checking its exit status"""
	return proc_check_output(cmd, shell = True, env = _setenv(env)).decode('utf-8')

def _sudo(cmd: str, args: str, timeout = system_ttl) -> int:
	x = f"/usr/bin/sudo -H -n -u uws -- {cmddir}/{cmd} {args}"
	return system(x.strip(), timeout = timeout)

def ctl(args: str, timeout: int = system_ttl) -> int:
	"""run internal app-ctl command"""
	debug('ctl:', args)
	return _sudo("app-ctl.sh", "%s %s" % (_user, args), timeout = timeout)

def nq(cmd: str, args: str, bindir: str = cmddir) -> int:
	"""enqueue internal command"""
	debug('nq:', cmd, args)
	return _sudo("uwsnq.sh", "%s %s/%s %s" % (_user, bindir, cmd, args))

def run(cmd: str, args: str, timeout: int = system_ttl) -> int:
	"""run internal command"""
	debug('run:', cmd, args)
	return _sudo(cmd, args, timeout = timeout)

def clean_build(app: str) -> int:
	"""enqueue build clean task"""
	debug('clean build:', app)
	return _sudo("uwsnq.sh", "%s %s/app-clean-build.sh %s" % (_user, cmddir, app))

#
# app list / description
#

def __descmax(k: list[str]) -> int:
	m = 0
	for s in k:
		l = len(s)
		if l > m:
			m = l
	return m

def __descsep(k: str, m: int) -> str:
	s = ' '
	for i in range(len(k), m):
		s += ' '
	return s

def __desc(apps: list[str]) -> str:
	m = __descmax(apps)
	d = 'available apps:\n'
	for n in apps:
		d += "  %s%s- %s\n" % (n, __descsep(n, m), app[n].desc)
	return d

def app_list() -> list[str]:
	"""return list of configured apps"""
	return user_auth(_user, [n for n in app.keys() if app[n].app])

def app_description() -> str:
	"""format apps list description"""
	return __desc(app_list())

def app_groups() -> list[str]:
	"""return list of app groups"""
	g: dict[str, bool] = {}
	for n in app.keys():
		for gn in app[n].groups:
			g[gn] = True
	return sorted(g.keys())

def autobuild_list() -> list[str]:
	"""return list of apps configured for autobuild"""
	return user_auth(_user, [n for n in app.keys() if app[n].build and app[n].autobuild])

def autobuild_description() -> str:
	"""format apps autobuild list description"""
	return __desc(autobuild_list())

def autobuild_deploy(n: str) -> list[str]:
	"""get list of apps to deploy from an autobuild"""
	return app[n].autobuild_deploy.copy()

def build_list(user: User | None = None) -> list[str]:
	"""return list of apps configured for build"""
	if user is None: user = _user
	return user_auth(user, [n for n in app.keys() if app[n].build.dir != ''])

def build_description() -> str:
	"""format build apps description"""
	return __desc(build_list())

def build_blacklist(appname: str, tag: str) -> bool:
	"""check if the version is blacklisted to be built"""
	if appname in app.keys():
		if tag.strip() in app[appname].build_blacklist:
			return True
	return False

_buildpack_version_re = re.compile('.*-bp\d+$')

def _image_version(v: str) -> str:
	if _buildpack_version_re.match(v):
		return '-'.join(v.split('-')[:-1])
	return v

def build_done(appname: str, tag: str) -> bool:
	"""check against images repo if it already exists"""
	debug("build_done check:", appname, tag)
	for i in list_images(appname, region = 'us-east-1'):
		debug("built image:", i)
		if i.startswith(tag):
			v = _image_version(i)
			debug("image version:", i, v)
			if v == tag:
				debug("build_done check:", appname, tag, v, "done!")
				return True
	debug("build_done check:", appname, tag, "NOT done!")
	return False

def deploy_list(user: User | None = None) -> list[str]:
	"""return list of apps configured for deploy"""
	if user is None: user = _user
	return user_auth(user, [n for n in app.keys() if app[n].deploy.image != ''])

def deploy_description() -> str:
	"""format deploy apps description"""
	return __desc(deploy_list())

from uwscli_conf import CustomDeploy

def custom_deploy(appname: str, env: str) -> list[CustomDeploy]:
	"""return app custom deploy configuration"""
	if not appname in app.keys():
		return []
	return app[appname].custom_deploy.get(env, [])

#
# aws utils
#

def list_images(appname: str, region: str = '') -> list[str]:
	"""get aws ECR list of available app images"""
	debug("list_images:", appname, region)
	if app[appname].deploy_app != '':
		orig = appname.strip()
		appname = app[appname].deploy_app.strip()
		debug("list_images:", orig, "deploy_app", appname)
	kn = app[appname].cluster
	if region == '':
		try:
			region = cluster[kn].region
		except KeyError:
			error(f"{kn}: no cluster region to list images")
			return []
	debug("list_images:", appname, region)
	deploy_image = app[appname].deploy.image.strip()
	deploy_filter = app[appname].deploy.filter.strip()
	if deploy_image == '':
		error("list_images:", appname, "empty deploy.image")
		return []
	if deploy_filter == '':
		error("list_images:", appname, "empty deploy.filter")
		return []
	cmd = "aws ecr list-images --output text --repository-name uws"
	cmd += " --region %s" % region
	cmd += " | grep -F '%s'" % deploy_image
	cmd += " | awk '{ print $3 }'"
	cmd += " | sed 's/^%s//'" % deploy_filter
	cmd += " | sort -V"
	try:
		debug("list_image:", cmd)
		out = check_output(cmd)
		return out.splitlines()
	except CalledProcessError as err:
		error(f"[ERROR] {appname} list images: {err.output}")
	return []

#
# git utils
#

def git_clone(rpath: str) -> int:
	"""git clone"""
	return system(f"git clone {rpath}")

def git_fetch(workdir: str = '.') -> int:
	"""git fetch"""
	args = ''
	if workdir != '.':
		args += f" -C {workdir}"
	return system(f"git{args} fetch --prune --prune-tags --tags")

def git_checkout(tag: str, workdir: str = '.') -> int:
	"""git checkout"""
	args = ''
	if workdir != '.':
		args += f" -C {workdir}"
	return system(f"git{args} checkout {tag}")

def git_deploy(rname: str, tag: str) -> int:
	"""run uwscli deploy"""
	return uwscli_deploy.run(rname, tag)

def git_describe(workdir: str = '.') -> str:
	"""git describe"""
	args = ''
	if workdir != '.':
		args += f" -C {workdir}"
	return check_output(f"git{args} describe --always").strip()

def git_tag_list(workdir: str = '.') -> list[str]:
	"""git tag --list"""
	args = ''
	if workdir != '.':
		args += f" -C {workdir}"
	return check_output(f"git{args} tag --list").strip().split(sep = linesep)
