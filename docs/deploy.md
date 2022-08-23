# Infrastructure Deploy

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
