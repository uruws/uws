# TODO

## live changelog

* [Infrastructure](../../../compare/8035cc33...master)
* [MonitoringBots](../../../../MonitoringBots/compare/3cc8daf5...master)
* [munin-contrib](https://github.com/munin-monitoring/contrib/compare/master...uruws:master)

## 0315

* Mail smarthost service.
* Develop packaging tools.
	* Use bots deployment as alpha and beta testing for pkg tools.
* Build package ditribution repo(s).
	* The idea is to have some repos for:
		* pkg tools
		* common utils
		* services setup
		* common configs
		* host specific configs
* Develop servers CA certs manager web interface.
	* So authorized people can get their certs using email validation.
* Packaging tools.
	* Migrate current munin and munin-nodes setup to pkg tools.
		* So it can in the future be deployed to other server if needed.
		* Also to keep developing/improving/fixing bugs of pkg tools.
* Setup web servers load balancer and caching cluster.
	* Maybe use varnish as load balancer and cacher to put in front of apps containers?
	* Maybe use nginx for lb and caching?
	* Maybe use nginx as lb and varnish as cacher?
* Setup infra to deploy Pacemaker clusters.
	* The cluster will manage a swarm cluster of docker apps?
	* Directly manage the containers from pcmk?
	* Use remote nodes to bypass the 16 nodes limit:
		* virtual nodes?
		* dockerized nodes?
		* phisycal nodes?
		* phisycal nodes with virtual or docker nodes?
* fail2ban setup for already in production services: ssh and http(s)
	* ssh is already enabled by default on Debian (but we should check).
	* http(s) need some extra setup as we run the web services inside containers.
* Develop server tasks control.
	* The idea is to have a tiny web interface on servers so auth people can dispatch pre-configured tasks/jobs on the server. Like start/stop of containers and such.
