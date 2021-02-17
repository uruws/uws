# TODO

## 0215

* Setup monitoring of current mongodb and heroku infra.
* Develop monitoring bots.
	* The idea is to have scriptable bots to test/graph/monitor use case scenarios for production services. Starting with the API.
* Develop munin plugins for bots info.
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
* Mail smarthost docker service.
