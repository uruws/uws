# TODO

## live changelog

* [Infrastructure](../../../compare/86a9b4db...master)
* [MonitoringBots](../../../../MonitoringBots/compare/4bad28e9...master)

## 0222

* Develop munin plugins for bots info.
* Develop servers CA certs manager web interface.
	* So authorized people can get their certs using email validation.
* Develop packaging tools.
	* Use bots deployment as alpha and beta testing for pkg tools.
* Build package ditribution repo(s).
	* The idea is to have some repos for:
		* pkg tools
		* common utils
		* services setup
		* common configs
		* host specific configs
* Develop server tasks control.
	* The idea is to have a tiny web interface on servers so auth people can dispatch pre-configured tasks/jobs on the server. Like start/stop of containers and such.
* Packaging tools.
	* Migrate current munin and munin-nodes setup to pkg tools.
		* So it can in the future be deployed to other server if needed.
		* Also to keep developing/improving/fixing bugs of pkg tools.
* fail2ban setup for already in production services: ssh and http(s)
	* ssh is already enabled by default on Debian (but we should check).
	* http(s) need some extra setup as we run the web services inside containers.
* Setup monitoring of current mongodb and heroku infra.
* Mail smarthost docker service.
