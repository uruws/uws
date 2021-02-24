# Batch processing server

[jsbatch](https://jsbatch.uws.talkingpts.org/)

We built a server in AWS `us-west-1` region to run batch processes.

The idea is to have an infrastructure to run db analysis procs in paralell,
using docker containers.

[AWS console](https://us-west-1.console.aws.amazon.com/ec2/v2/home?region=us-west-1#InstanceDetails:instanceId=i-0657e7fbe7c1f8ef2)

Some [docs](https://github.com/TalkingPts/Analysis/blob/iss72/docker/iss72/README.md) about the setup.

## Deploy

* [config](../../host/config/61_jsbatch_setup.cfg)
* [assets](../../host/assets/jsbatch/)
* repo: `uws@jsbatch.uws.talkingpts.org:/srv/uws/deploy.git`
