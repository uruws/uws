# DONE

* [AWS infra](./infra/aws.md)
* [Service container](./service/container.md)
* [DevOps](./devops.md)
* Batch processing server: [jsbatch](https://jsbatch.uws.talkingpts.org/)
* Monitoring:
	* Bot engine: [uwsbot](./uwsbot.md)
	* Bot scripts repo: [MonitoringBots][monbots.repo]

[monbots.repo]: https://github.com/TalkingPts/MonitoringBots

## 0315

* Patched munin contrib mongodb plugins and propose them to upstream.
	* [fix](https://github.com/munin-monitoring/contrib/pull/1189) mongo_collection_.
	* [pu](https://github.com/munin-monitoring/contrib/pull/1190) MONGO_DB_URI env config.
	* [pu](https://github.com/munin-monitoring/contrib/pull/1191) configurable graph_category.

## 0308

* Released [uwsbot v0.1](../../../releases/tag/release%2Fuwsbot-v0.1).
* Setup monitoring of current mongodb and heroku infra.
	* We created a testing env on our aws infra using the built app from heroku staging.
	* We also enabled some munin checks against the container running the app.
	* We also enabled some checks against mongodb servers, which are still hosted outside.

### ChangeLog

* [Infrastructure](../../../compare/867502b1...8035cc33)
* [MonitoringBots](../../../../MonitoringBots/compare/f71731f2...3cc8daf5)

## 0301

* Improve munin bots graphs to get detailed POST/GET info.
* Setup api bot for staging and production envs.
* Develop next round of api scripts.

### ChangeLog

* [Infrastructure](../../../compare/cd5a455c...867502b1)
* [MonitoringBots](../../../../MonitoringBots/compare/56080e41...f71731f2)

# Archive

* [202102](./archive/2021/02/202102-done.md)
