# DONE

## AWS

* Amazon account: [789470191893][awsorg]
* Main region used for devops infra: us-east-1

## Admin

* [IAM uwsadm][uwsadm]:

All the infrastructure managed using AWS services is owned by **uwsadm** IAM
user.

## DNS

* [Route53][uwsdns] hosted zones.

The main domain used for devops is **uws.talkingpts.org** and it's hosted using
AWS Route53 service.

## EC2

* AMI used as base installation for *ALL* instances: [debian-base][uwsami].
* [GNU/Linux Debian](https://www.debian.org) is used as main OS.
* Current OS version: 10 (Buster).
* Instance launch template: [uws-debian-base][uwsinstall-tpl].

## Networking

Addresses allocated using AWS EC2 elastic IP:

* [54.204.105.139][janisip]: uws.talkingpts.org janis.uws.talkingpts.org

## Service container

Services are deployed to EC2 instances using [Docker](https://www.docker.com/)
containers.

* Base docker image definition: [docker/base](./docker/base/Dockerfile).
* Services image definition:
	* [acme](./srv/acme/Dockerfile): [Let's Encrypt](https://letsencrypt.org/) auto SSL certificates management using [acme-tiny](https://github.com/diafygi/acme-tiny).
	* [munin](./srv/munin/Dockerfile): [munin](http://munin-monitoring.org/) monitors and graphs network resources.

[awsorg]: https://console.aws.amazon.com/organizations/home
[uwsadm]: https://console.aws.amazon.com/iam/home?region=us-east-1#/users/uwsadm
[uwsdns]: https://console.aws.amazon.com/route53/v2/hostedzones
[uwsami]: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Images:sort=name
[janisip]: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#ElasticIpDetails:AllocationId=eipalloc-0c5ae6d42089a8328
[uwsinstall-tpl]: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LaunchTemplateDetails:launchTemplateId=lt-018d4b7d7e51c55c4
