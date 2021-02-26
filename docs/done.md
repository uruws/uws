# DONE

* [AWS infra](./infra/aws.md)
* [Service container](./service/container.md)
* [DevOps](./devops.md)
* Batch processing server: [jsbatch](https://jsbatch.uws.talkingpts.org/)
* Monitoring:
	* Bot engine: [uwsbot](./uwsbot.md)
	* Bot scripts repo: [MonitoringBots][monbots.repo]

[monbots.repo]: https://github.com/TalkingPoints/MonitoringBots

## 0222

* Fix docker_network bug. No graphs are being created do to config errors.
	* https://github.com/munin-monitoring/contrib/issues/1182
* Develop monitoring bots.
	* The idea is to have scriptable bots to test/graph/monitor use case scenarios for production services. Starting with the API.

## 0201

[ChangeLog](../../../compare/0b050354...86a9b4db)

* Initial commit up to 20210222 (316 commits).
