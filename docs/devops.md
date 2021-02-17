# DevOps

* [uws.t.o][uws] devops website.
* [Janis][janis.uws] is the main server for managing the infrastructure.
	* Services:
		* [munin][munin]
		* munin-nodes: www and app
		* build and deploy infra from git repo
		* packaging main repo and builder

### Devops: host deploy

Host deploy to EC2 instances is being done using [cloud-init][cloud-init-20.2] (v20.2) system.

* Deploy host configs: [host/config](../host/config)
* Deploy host assets: [host/assets](../host/assets)
* Deploy script: [host/deploy.sh](../host/deploy.sh)

Deploys can be done manually (if you have the right accesses) using
`host/deploy.sh` or a full deploy of the infra can be done via a push to the
git repostitory `uws@uws.talkingpts.org:/srv/uws/deploy.git` hosted at *janis*.

* Git update hook: [janis/uws/git-uws-update.sh](../host/assets/janis/uws/git-uws-update.sh)
* Git deploy script: [janis/uws/git-uws-deploy.sh](../host/assets/janis/uws/git-uws-deploy.sh)

### Devops: packaging system

We use [FreeBSD packaging system][pkgng] for internal software and configuration
distribution.

It's being developed in a separate repository: [TalkingPts/Packaging][tpts.pkg].



[uws]: https://uws.talkingpts.org
[janis.uws]: https://janis.uws.talkingpts.org

[munin]: https://uws.talkingpts.org/munin/
[cloud-init-20.2]: https://cloudinit.readthedocs.io/en/20.2/

[pkgng]: https://github.com/freebsd/pkg
[tpts.pkg]: https://github.com/TalkingPts/Packaging
