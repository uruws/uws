# DONE

* [AWS infra](./infra/aws.md)
* [Service container](./service/container.md)
* [DevOps](./devops.md)
* Batch processing server: [jsbatch](https://jsbatch.uws.talkingpts.org/)
* Monitoring:
	* Bot engine: [uwsbot](./uwsbot.md)
	* Bot scripts repo: [MonitoringBots][monbots.repo]

[monbots.repo]: https://github.com/TalkingPts/MonitoringBots

## 0222

* Fix docker_network bug. No graphs are being created do to config errors.
	* https://github.com/munin-monitoring/contrib/issues/1182
* Develop monitoring bots.
	* The idea is to have scriptable bots to test/graph/monitor use case scenarios for production services. Starting with the API.
* Develop munin plugins for bots info.

### ChangeLog

* [Infrastructure](../../../compare/86a9b4db...cd5a455c)
* [MonitoringBots](../../../../MonitoringBots/compare/4bad28e9...56080e41)

## 0201

[ChangeLog](../../../compare/0b050354...86a9b4db)

* Initial commit up to 20210222 (316 commits).
