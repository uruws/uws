# TODO

## 0222

* Activity Log:
	* [Infrastructure](/TalkingPts/Infrastructure/compare/86a9b4db...master)
	* [MonitoringBots](/TalkingPts/MonitoringBots/compare/4bad28e9...master)

* Develop monitoring bots.
	* The idea is to have scriptable bots to test/graph/monitor use case scenarios for production services. Starting with the API.
* Setup monitoring of current mongodb and heroku infra.
* Develop servers CA certs manager web interface.
	* So authorized people can get their certs using email validation.
* Develop munin plugins for bots info.
* Develop server tasks control.
	* The idea is to have a tiny web interface on servers so auth people can dispatch pre-configured tasks/jobs on the server. Like start/stop of containers and such.
* Develop packaging tools.
	* Use bots deployment as alpha and beta testing for pkg tools.
	* Then migrate current munin and munin-nodes setup to pkg tools.
		* So it can in the future be deployed to other server if needed.
		* Also to keep developing/improving/fixing bugs of pkg tools.
* Build package ditribution repo(s).
	* The idea is to have some repos for:
		* pkg tools
		* common utils
		* services setup
		* common configs
		* host specific configs
* fail2ban setup for already in production services: ssh and http(s)
	* ssh is already enabled by default on Debian (but we should check).
	* http(s) need some extra setup as we run the web services inside containers.
* Mail smarthost docker service.
