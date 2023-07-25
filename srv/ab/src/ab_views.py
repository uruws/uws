# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import subprocess

import wapp

import ab

log = wapp.getLogger(__name__)

#-------------------------------------------------------------------------------
# /healthz

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

#-------------------------------------------------------------------------------
# /run/

def run():
	return wapp.template('ab/run.html')

def run_post():
	try:
		url = 'https://%s' % wapp.request.POST.get('abench_url', 'NO_URL')
		cmd = ab.Command(url)
		job = cmd.run()
	except Exception as err:
		log.error('%s', err)
		return wapp.error(500, 'ab/error.html', app = wapp.name, error = str(err))
	if job.rc() != 0:
		log.error('command failed (%d): %s', job.rc(), job.error())
		return wapp.error(500, 'ab/error.html', app = wapp.name, error = 'command failed: %d' % job.rc())
	return wapp.redirect(wapp.url('/nq/'))

#-------------------------------------------------------------------------------
# /nq/

def _nqjobs():
	q = wapp.NQ('run')
	jobs = []
	for j in reversed(q.list()):
		jobs.append(ab.command_parse(j.id(), str(j)))
	return jobs

def nq():
	return wapp.template('ab/nq.html',
		abench_nqjobs = _nqjobs(),
	)

def nq_job(jobid: str):
	q = wapp.NQ('run')
	try:
		text = q.read(jobid)
	except FileNotFoundError as err:
		log.error('%s', err)
		return wapp.error(404, 'ab/error.html', app = wapp.name, error = '%s' % err)
	return wapp.template('ab/nq_job.html',
		job_id     = jobid,
		job_output = text,
	)

#-------------------------------------------------------------------------------
# /

def home():
	return wapp.template('ab/home.html',
		abench_nqjobs = _nqjobs(),
	)

#-------------------------------------------------------------------------------
# main

def start(app: wapp.Bottle):
	# /healthz
	app.get(wapp.url('/healthz'), callback = healthz)
	# /run/
	app.get(wapp.url('/run/'),  callback = run)
	app.post(wapp.url('/run/'), callback = run_post)
	# /nq/
	app.get(wapp.url('/nq/'),        callback = nq)
	app.get(wapp.url('/nq/<jobid>'), callback = nq_job)
	# /
	app.get(wapp.url('/'), callback = home)
