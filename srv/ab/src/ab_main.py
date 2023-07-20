# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import wapp

import ab
import ab_conf

app = wapp.Bottle()
log = wapp.getLogger(__name__)

#
# views
#

@app.get('/healthz')
def healthz():
	wapp.response.content_type = 'text/plain'
	cmd = ab.Command('--help')
	rc = ab.run(cmd)
	if rc != 22:
		raise RuntimeError('ab exit status: %d' % rc)
	return 'ok'

@app.get('/run/')
def run():
	return wapp.template('ab/run.html')

@app.post('/run/')
def run_post():
	try:
		q = wapp.NQ('run')
		job = q.run([ab.cmdpath.as_posix()])
	except Exception as err:
		log.error('%s', err)
		return wapp.template('error.html', app = 'ab', error = str(err))
	if job.rc() != 0:
		return wapp.template('error.html', app = 'ab', error = 'command failed: %d' % job.rc())
	return wapp.template('ab/nq.html')

@app.get('/')
def home():
	return wapp.template('ab/home.html')

#
# main
#

def start():
	wapp.start(app)
	log.debug('start')

def wsgi_application():
	start()
	log.debug('wsgi app')
	return app

def main():
	start()
	log.debug('bottle run')
	wapp.run(app)

if __name__ == '__main__': # pragma: no cover
	main()
