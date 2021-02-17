# Service container

Services are deployed to EC2 instances using [Docker](https://www.docker.com/)
containers.

* Base docker image definition: [docker/base](../../docker/base/Dockerfile).
* Containers are deployed using AWS ECR private/internal docker hub: [uws][uwsecr].
* Services image definition:
	* [acme](../../srv/acme/Dockerfile): [Let's Encrypt](https://letsencrypt.org/) auto SSL certificates management using [acme-tiny](https://github.com/diafygi/acme-tiny).
	* [munin](../../srv/munin/Dockerfile): [munin](http://munin-monitoring.org/) monitors and graphs network resources.



[uwsecr]: https://console.aws.amazon.com/ecr/repositories/private/789470191893/uws?region=us-east-1
