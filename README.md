# uws

Uruworks sysadmin tools for Talking Points infrastructure.

* [TODO](./docs/todo.md)
* [CLI](./docs/devops.md) devops tools.
* [Heroku](./docs/heroku.md) contingency plan.
* Infra
	* [Upgrades](./docs/infra/upgrades.md)
* Network topology
	* [App](./docs/topology/app.png)

## Clusters

* [amy](./cluster/amy/README.md): App web service and workers.
	* `./eks/admin.sh amy-east`
	* `./eks/admin.sh amy-west`
	* `./eks/admin.sh amy-wrkr`
* [amybeta](./cluster/amybeta/README.md): App beta and Crowdsourcing web services.
	* `./eks/admin.sh amybeta`
* [panoramix](./cluster/panoramix/README.md): NLP service.
	* `./eks/admin.sh panoramix`
