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
	return wapp.template('ab/run.html', abench_nqjobs_form = ab.CommandForm())

def run_post():
	try:
		cmd = ab.CommandForm().parse(wapp.request.POST)
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

def _nq() -> wapp.NQ:
	return wapp.NQ('run')

def _nqjobs():
	q = _nq()
	jobs = []
	for j in reversed(q.list()):
		jobs.append(ab.command_parse(j.id(), str(j)))
	return jobs

def nq():
	return wapp.template('ab/nq.html',
		abench_nqjobs = _nqjobs(),
	)

def nq_job(jobid: str):
	q = _nq()
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
# /nq.delete/

def nq_delete(jobid: str):
	job = ab.command_parse(jobid, '')
	return wapp.template('ab/job_delete.html', job = job)

def nq_delete_post(nq = None):
	q = _nq()
	if nq is not None:
		del q
		q = nq
	try:
		jobid = wapp.request.POST.get('abench_jobid', '')
		q.rm(jobid)
	except Exception as err:
		log.error('%s', err)
		return wapp.error(404, 'ab/error.html', app = wapp.name, error = '%s' % err)
	return wapp.redirect(wapp.url('/nq/'))

#-------------------------------------------------------------------------------
# /nq.exec/

def nq_exec(jobid: str):
	job = ab.command_parse(jobid, '')
	return wapp.template('ab/job_exec.html', job = job)

def nq_exec_post(nq = None):
	q = _nq()
	if nq is not None:
		del q
		q = nq
	try:
		jobid = wapp.request.POST.get('abench_jobid', '')
		job = q.exec(jobid)
	except Exception as err:
		log.error('%s', err)
		return wapp.error(404, 'ab/error.html', app = wapp.name, error = '%s' % err)
	if job.rc() != 0:
		log.error('command failed (%d): %s', job.rc(), job.error())
		return wapp.error(500, 'ab/error.html', app = wapp.name, error = 'command failed: %d' % job.rc())
	return wapp.redirect(wapp.url('/nq/'))

#-------------------------------------------------------------------------------
# /

def home():
	return wapp.template('ab/home.html',
		abench_nqjobs      = _nqjobs(),
		abench_nqjobs_form = ab.CommandForm(),
	)

#-------------------------------------------------------------------------------
# main

def start(app: wapp.Bottle):
	# /healthz
	app.get(wapp.url('/healthz'), callback = healthz)
	# /run/
	app.get(wapp.url('/run/'),  callback = run)
	app.post(wapp.url('/run/'), callback = run_post)
	# /nq.delete/
	app.post(wapp.url('/nq.delete/'),       callback = nq_delete_post)
	app.get(wapp.url('/nq.delete/<jobid>'), callback = nq_delete)
	# /nq.exec/
	app.post(wapp.url('/nq.exec/'),       callback = nq_exec_post)
	app.get(wapp.url('/nq.exec/<jobid>'), callback = nq_exec)
	# /nq/
	app.get(wapp.url('/nq/'),        callback = nq)
	app.get(wapp.url('/nq/<jobid>'), callback = nq_job)
	# /
	app.get(wapp.url('/'), callback = home)
