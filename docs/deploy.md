# Infrastructure Deploy

## Manually

If not done already, configure the deploy repository first:

	$ git remote add deploy uws@ops.uws.talkingpts.org:/srv/uws/deploy.git

Then commit, push and deploy:

	$ git commit ...
	$ git push
	$ git push deploy

To check the deploy log SSH to the ops server:

	$ ssh -l uws ops.uws.talkingpts.org

And check the log file under `/var/tmp/uws-deploy.log`

	$ tail -f /var/tmp/uws-deploy.log

## Automated

Or you can run the `deploy.sh` script which kind of automates the steps above.

To run the tests locally first, deploy and follow the log, run:

	$ ./deploy.sh

You have to finish it with *CTRL+C*.

Avoid running tests locally with:

	$ ./deploy.sh --no-test

Avoid following the deploy log with:

	$ ./deploy.sh --no-logs
