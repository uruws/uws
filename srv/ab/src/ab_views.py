# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import subprocess

import wapp

import ab

log = wapp.getLogger(__name__)

#
# /healthz
#

def _check() -> int:
	cmd = ab.Command('--help')
	proc = subprocess.run(cmd.args(), check = False, timeout = 15, capture_output = True)
	if proc.returncode != 22: # pragma: no cover
		log.error('%s', proc.stderr.strip())
	return proc.returncode

def healthz():
	wapp.response.content_type = 'text/plain'
	cmd = ab.Command('--help')
	rc = _check()
	if rc != 22:
		raise RuntimeError('ab exit status: %d' % rc)
	return 'ok'

#
# /run/
#

def run():
	return wapp.template('ab/run.html')

def run_post():
	try:
		url = 'https://%s' % wapp.request.POST.get('abench_url', 'NO_URL')
		cmd = ab.Command(url)
		job = cmd.run()
	except Exception as err:
		log.error('%s', err)
		return wapp.template('error.html', app = wapp.name, error = str(err))
	if job.rc() != 0:
		log.error('command failed (%d): %s', job.rc(), job.error())
		return wapp.template('error.html', app = wapp.name, error = 'command failed: %d' % job.rc())
	return wapp.redirect(wapp.url('/nq/'))

#
# /nq/
#

def nq():
	q = wapp.NQ('run')
	return wapp.template('ab/nq.html',
		abench_nqjobs = q.list(),
	)

#
# /
#

def home():
	return wapp.template('ab/home.html')

#
# main
#

def start(app: wapp.Bottle):
	app.get( wapp.url('/healthz'), callback = healthz)
	app.get( wapp.url('/run/'),    callback = run)
	app.post(wapp.url('/run/'),    callback = run_post)
	app.get( wapp.url('/nq/'),     callback = nq)
	app.get( wapp.url('/'),        callback = home)
