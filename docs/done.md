# DONE

## AWS

* Main region used for devops infra: **us-east-1** *(N. Virginia)*

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

* [54.204.105.139][janisip]: [uws.t.o][uws] [janis.uws.t.o][janis.uws]

## Service container

Services are deployed to EC2 instances using [Docker](https://www.docker.com/)
containers.

* Base docker image definition: [docker/base](../docker/base/Dockerfile).
* Containers are deployed using AWS ECR private/internal docker hub: [uws][uwsecr].
* Services image definition:
	* [acme](../srv/acme/Dockerfile): [Let's Encrypt](https://letsencrypt.org/) auto SSL certificates management using [acme-tiny](https://github.com/diafygi/acme-tiny).
	* [munin](../srv/munin/Dockerfile): [munin](http://munin-monitoring.org/) monitors and graphs network resources.

## DevOps

* [uws.t.o][uws] devops website.
* [Janis][janis.uws] is the main server for managing the infrastructure.
	* Services:
		* smarthost mail server
		* munin
		* munin-nodes: www and app
		* build and deploy infra from git repo
		* main etcd node for infra config deployment

### Devops: host deploy

Host deploy to EC2 instances is being done using [cloud-init][cloud-init-20.2] (v20.2) system.

* Deploy host configs: [host/config](../host/config)
* Deploy host assets: [host/assets](../host/assets)
* Deploy script: [host/deploy.sh](../host/deploy.sh)

Deploys can be done manually (if you have the right accesses) using
`host/deploy.sh` or a full deploy of the infra can be done via a push to the
git repostitory `uws@uws.talkingpts.org:deploy.git` hosted at *janis*.

* Git update hook: [janis/uws/git-uws-update.sh](../host/assets/janis/uws/git-uws-update.sh)
* Git deploy script: [janis/uws/git-uws-deploy.sh](../host/assets/janis/uws/git-uws-deploy.sh)

[uws]: https://uws.talkingpts.org
[uwsadm]: https://console.aws.amazon.com/iam/home?region=us-east-1#/users/uwsadm
[uwsdns]: https://console.aws.amazon.com/route53/v2/hostedzones

[uwsami]: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Images:sort=name
[uwsinstall-tpl]: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LaunchTemplateDetails:launchTemplateId=lt-018d4b7d7e51c55c4
[uwsec2-role]: https://console.aws.amazon.com/iam/home?region=us-east-1#/roles/EC2InstanceRole

[uwsecr]: https://console.aws.amazon.com/ecr/repositories/private/789470191893/uws?region=us-east-1
[cloud-init-20.2]: https://cloudinit.readthedocs.io/en/20.2/

[janis.uws]: https://janis.uws.talkingpts.org
[janisip]: https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#ElasticIpDetails:AllocationId=eipalloc-0c5ae6d42089a8328
