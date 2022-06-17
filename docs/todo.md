* `URGENT` cluster stack - `WIP`
    * update tools to run kubernetes 1.22 (previous was 1.19) - `DONE!` [PR#9][PR#9]
    * migrate clusters
        * amy-test-1 and amy-test-2
            * apptest-east and apptest-west - `DONE!` [PR#11][PR#11]
            * migrated worker-test, cs-test and infra-ui-test - `DONE!` [PR#12][PR#12]
            * migrated apptest (staging.talkingpts.org) - `DONE!` [PR#13][PR#13]
        * remove 1.19 amy-wrkr cluster - `DONE!` [PR#14][PR#14]
    * rotate aws credentials in the process
    * create new clusters using spot nodegroups as suggested by AWS support people
        * EKS ec2 "reserved instances" setup to help saving costs

[PR#11]: https://github.com/TalkingPts/Infrastructure/pull/11
[PR#12]: https://github.com/TalkingPts/Infrastructure/pull/12
[PR#13]: https://github.com/TalkingPts/Infrastructure/pull/13
[PR#14]: https://github.com/TalkingPts/Infrastructure/pull/14

* workers k8s 1.22 version and nodes memory upgrade - `DONE!` [PR#9][PR#9] [PR#10][PR#10]
    * create and/or modify eks admin tools to support different kubernets versions
    * create workers 1.22 cluster (worker-2206)

[PR#9]: https://github.com/TalkingPts/Infrastructure/pull/9
[PR#10]: https://github.com/TalkingPts/Infrastructure/pull/10

* k8sctl: deprecate - `DONE!`
    * stop building it, but keep code and deploy files around for now

* remove old aws credentials once all cluster upgrades are finished

* Infrastructure deploy
    * restore deploy of only signed commits
    * we have to disable it so Aram is able to deploy changes
    * we should re-enable it and authorize Aram's GPG key

* infra-api - `WIP`
    * auth system - `DONE!`
    * help pages
    * make commands run using nq to avoid HTTP connections timeout
        * run commands using a per user NQDIR
        * schedule it and return its qid
        * job status/log API endpoints
    * testing deploy
    * building on [InfraApp][InfraApp] repository
        * Changelog: [master](https://github.com/TalkingPts/InfraApp/commits/master)

[InfraApp]: https://github.com/TalkingPts/InfraApp

* App encrypt secrets - `WAIT`
    * git-crypt setup for private/secrets directory [App PR#910][APP#910]
    * `WAIT` for dev team to do the private files migration
        * do we need to update the Buildpack for new private files location?

[APP#910]: https://github.com/TalkingPts/App/pull/910

* tapoS3Dev bucket for App local devel

* create a monitoring from App logs for Bandwidth message-failed like the one that follows.

    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059667535Z Bandwidth sms callback [
    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059715316Z   {
    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059722316Z     time: '2022-06-14T18:38:45.798Z',
    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059727236Z     type: 'message-failed',
    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059731996Z     to: '+12408057329',
    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059736966Z     description: '050003BA0303006F0077 Carrier error 503',

* `FIX` app-autobuild
    * keep track of tags already in the build queue, to avoid, in example:
        * 2.71.5 was dispatched as latest build was 2.71.3
        * 2.71.4 was dispatched manually by Gabriel so autobuild didn't knew
        * as 2.71.4 build was running and taking some time, 2.71.5 keeps being queued because latestBuild info keeps saying that it was 2.71.3 until 2.71.4 finish but still the same... 2.71.5 keeps being queued... etc...
    * based from a discussion with Gabriel about how to "better" implement it
        * autobuild deploys should only happend if we are deploying a newer version
        * that's because now ANY build dispatchs auto deploys for configured apps
        * we want the auto deploy functionallity from any kind of build
        * but taking care of the deploy
            * because it happens often that a build of an older sprint version is dispatched for a hotfix or whatever... we don't want to auto deploy those
            * autobuilds will always deploy new tags, but we need to fix it for manual dispatch

* `FIX` app-build
    * do not dispatch build if one already in place for same version

* `FIX` implement a "double check" mechanism for changing DNS uws.t.o domain records
    * the idea is to avoid issues like the one I did changing a production record
    * maybe use an script for Route53 editions which alerts about prod domains or similar
    * try to avoid manual changes (maybe some peer review?)

* uwscli auto-setup from main configuration
    * integrate with buildpack deploy scripts

* munin: scan cluster ingress domains and add them to the checks (munin-node-clusters)

* aws support meeting
    * setup CDN mainly to help saving network transfer costs
    * Route53 app.t.o use geolocation inside US or latency setup
        * versus current weighted 50/50 setup
        * we must keep the "heroku contingency plan" setup or adapt it to new ways

* add bot to check we can send emails? (mandrill service)

* `CLEAN` /srv/deploy/analysis.git setup for (old) iss72 deploy

* `FIX` buildpack:
    * use tag version from command line for publishing the image
    * instead of using the git describe tag
    * currently if a commit has more than one tag associated build fails because previous version already exists
    * that or fix the git describe command to get latest tag instead of first one

    tag invalid: The image tag 'meteor-app-2.64.7-bp21' already exists in the
    'uws' repository and cannot be overwritten because the repository is immutable.

    Publish app version 2.64.8 failed

* uwscli:
    * app-autobuild: nq build and deploy jobs
    * cli/buildpack.sh: should manage the log and email report if any fail
    * cli/app-build.sh: should do the same
    * `FIX` app-autobuild: when jsbatch is restarted autobuild of last tag fails
        * because the image already exists in the ECR
        * as /run/uwscli/build/app.status is with a failed state it keeps trying (looping) and failing every 15min...
        * maybe add an @reboot job to se app.status accordingly? set a BOOT state or similar?
        * if .status file is not find assume it was built and do nothing?
        * and/or check the going to be built tag exists in the ECR?
    * app-deploy:
        * list available builds using semver sort order

* uwsq: clean failed jobs

* `SEC` mongodb credentials rotation schedule

* `SEC` aws auth credentials rotation schedule
    * uwsadm and friends "access keys"

* mongodb analyzer?

* app-autobuild deploy
    * wait some time between deploys on "multi cluster" apps

* munin
    * graphs and limits/alerts about HTTP "error status ratio"
        * aka: ratio between failed (!=200) vs ok (==200)status
    * cluster cross check k8sctl service

* munin pods_container (check phase)
    "status": {
        "message": "The node was low on resource: memory. Container controller was using 2391212Ki, which exceeds its request of 90Mi. ",
        "phase": "Failed",
        "reason": "Evicted",
        "startTime": "2022-02-09T03:24:23Z"
    }

* munin alerts to slack
    * setup/devel bot
    * remove setup munin limit mail alerts
        * dev_ops_vo548nvb
            * munin-alerts TO
            * gmail fetch
            * create forward rules to slack and others

* nlpsvc: separate apps namespaces (for graphs and cli status/logs)

* rstudio checks
    * http_loadtime IDE and Jupyter Notebook from jsbatch
    * vm local munin setup (ansible role)

* ansible roles
    * monit
        * setup monit to check fail2ban keeps running
        * and others...
    * fail2ban
    * munin

* non-prod sites robots.txt to disallow all crawlers?

* WAF setup
    * implement fail2ban for kubernets/aws?
    * nginx modsecurity
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/configmap.md#enable-modsecurity
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md#modsecurity

* infra docs for internal presentation

* `FIX` k8smon: munin-alerts volume setup
    * until we can fix the volumes claim config, we could use one of the already existent volumes and set ALERTS_QDIR to point to it

* k8smon check jobs errors and sendmail.py if any (devel a munin plugin maybe?)
    * aws AMI nodegroup auto upgrade (should be a daily check)

* uwscli wish list
    * cleanup old images in ECR
    * app-build
        * we should be able to properly stop/abort a building process
    * show events log or auto-refresh status info
    * control deploy replicas
    * show web proxy logs

* cache web assets
    * use separate domain for static assets
    * test meteor appcache

* block web access by geoip?
    * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/configmap.md#use-geoip

* munin
    * graph app number of active users/sessions

* web deploy autoscale setup on custom metrics

* nginx
    * split cluster load over N instances instead of only 1
    * run them in their own node group?
    * or tune mem and cpu resources to make them run in a "dedicated" node?

* improve web deploys
    * currently it seems that the autoscaler moves around the pods after the deploy so it can re-arrange them in the minimun number of nodes as possible... In that sometimes the nginx-ingress pod is moved around so there's an outage there as the proxy is not available.
    * some ideas:
        * use more than one ingress (maybe in sep namespaces)
        * use different nodegroups for "core" services like nginx and the "main" nodegroup to run our services (web, workers, etc...), using node affinity annotations.
