# AWS

## Regions

* Main region used for devops infra: **us-east-1** *(N. Virginia)*
* [jsbatch][jsbatch.uws] region: **us-west-1** *(N. California)*
	* Used for batch processing against mongodb, using Google's bigquery service.
	* Those services are hosted near to (or at) this location, so we use this region for that.

## Admin

* [IAM uwsadm][uwsadm].

All the AWS infrastructure is owned by **uwsadm** IAM user.

## DNS

* [Route53][uwsdns].

The main domain used for devops is [uws.talkingpts.org][uws] and it's hosted
using AWS Route53 service.

## EC2

[GNU/Linux Debian](https://www.debian.org) is used as the main OS.

Current OS version: Debian 10 (Buster).

* AMI used as base installation for *ALL* instances: [debian-base][uwsami].
* Instance launch template: [uws-debian-base][uwsinstall-tpl].
* All instances run with [EC2InstanceRole][uwsec2-role] privileges.

## Networking

Addresses allocated using AWS EC2 elastic IP:

* us-east-1:
	* [54.204.105.139][janisip]: [uws.t.o][uws] [janis.uws.t.o][janis.uws]

* us-west-1:
	* [50.18.246.15][jsbatchip]: [uws.t.o][uws] [jsbatch.uws.t.o][jsbatch.uws]



[uws]: https://uws.talkingpts.org
[uwsadm]: https://console.aws.amazon.com/iam/home?region=us-east-1#/users/uwsadm
[uwsdns]: https://console.aws.amazon.com/route53/v2/hostedzones

[uwsami]: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Images:sort=name
[uwsinstall-tpl]: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LaunchTemplateDetails:launchTemplateId=lt-018d4b7d7e51c55c4
[uwsec2-role]: https://console.aws.amazon.com/iam/home?region=us-east-1#/roles/EC2InstanceRole

[janis.uws]: https://janis.uws.talkingpts.org
[janisip]: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#ElasticIpDetails:AllocationId=eipalloc-0c5ae6d42089a8328

[jsbatch.uws]: ./jsbatch.md
[jsbatchip]: https://us-west-1.console.aws.amazon.com/ec2/v2/home?region=us-west-1#ElasticIpDetails:AllocationId=eipalloc-d4486fe4
