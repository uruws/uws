* kubeshark 39.5 setup - `DONE!` [PR#138][PR#138]

[PR#138]: https://github.com/TalkingPts/Infrastructure/pull/138

---

* munin: new custom nginx metrics

---

* grafana.com integration setup

---

* uwscli new build/console server
    * run autobuilds there
    * with more CPU and MEM
    * do we move uwscli tools to there?
    * or do we make app-build dispatch the build on the build server?

---

* uwscli: nq deploy so once they start can not be stopped by ctrl+c or similar
    * we mainly need it for when custom deploys are launched
    * so maybe we have to nq deploys and also the custom deploy too

---

* munin: sendmail errors
    * uws@jsbatch:/srv/munin/var/alert/statuspage
    * check sendmail.log for errors
    * list queded .eml files

---

* munin: check nightly SIS sync's [DEV-4288][DEV-4288]
    * add it to statuspage alerts too

[DEV-4288]: https://talkingpointsorg.atlassian.net/browse/DEV-4288

---

* munin: check that App response headers include the "security headers" we need for SOC2
    * https://staging.t.o/login
        * Content-Security-Policy
        * Cross-Origin-Resource-Policy
        * Access-Control-Allow-Origin
        * Referrer-Policy

---

* munin: alert about workers callback http errors [worker-errors][worker-errors]
    * warning at 3 errors per minute
    * critical at 5 errors per minute
    * send alert to status page

[worker-errors]: https://worker-2209.uws.talkingpts.org/munin/uws/worker-2209/web_request_worker_uws_talkingpts_org/errors_per_minute.html

---

* Infrastructure CI: check-secret
    * check/parse config files from secret directory
        * like parsing secret/eks/files/meteor/*/*.json for syntax errors
        * secret/eks/files/meteor/*/*.env shellcheck and/or similar
        * secret/aws.config/s3/*.env and secret/aws.config/s3/*.json
        * secret/eks/files/munin/conf/alerts_conf.json

---

* `SEC` `WAIT` App security changes
    * Remove private/settings.json from the repo

---

* `SEC` `FIX` Firebase content is discoverable:
    * https://firebasestorage.googleapis.com/v0/b/talkingpnts.appspot.com/o/
    * working in an unrelated issue with Gabriel we found out that ^
    * we should use a CDN for that too, and avoid this issue and also improve performance and costs

---

* munin cluster's storage archive/sync to jsbatch or similar
    * for archiving/history and backup purposes
    * also to have some data available in case of the cluster being down
        * even if it will be old data, could be useful still
    * graph for nodes region/zones
    * nodes types
        * pass INSTANCE_TYPES env var to munin-node and keep them in the graph
    * graphs for PVs/PVCs?
        * available storage
        * region/zones

---

* app-autoscale
    * implement auto scaler based on custom metrics
        * web: scale based on web traffic/requests per minute
            * more or less, nowadays, 10 containers to serve 1000 rpm
            * [DB query](./worker-check-scheduled-jobs.txt)
        * workers:
            * cleverSynch could/should be another metric as it needs to finish before 10hs UTC
            * messages.jobs ready?
            * one metric could be based on checking scheduled district jobs to scale up before it starts, instead of reacting to an alert

---

* forensics setup

---

* munin: MongoDB slow queries

---

* CA rotate ops/210823

---

* `FIX` infra-ui config: JIRA_TOKEN='mauro'
    * and the JIRA_TOKEN too as I guess it's from Mauro's account
    * asked Gabriel but no reply yet

---

* Research Team
    * re-implement jupyter notebook setups
        * setup one web interface per user vs the "global" one we currently have

---

* munin
    * graph/check nodegroup status (alert when it's DEGRADED or not ACTIVE)
    * uwseks get nodegroup -n main -o json
    * check that munin-node container/service is running via k8smon "proxy"

---

* implement [node inspector][node-inspector] setup using the SSH approach
    * the idea is to have a way to dispatch "debugging containers" which could be inspected using chrome dev tools or similar, using the SSH tunneling setup as it seems to be the more secure for our infra
    * the SSH service should be only enabled when we dispatch the debug containers, using a random public port ideally and setting a random password for the uws user inside the container (show that password in the container init steps or similar) so we can share that info (port and password) "securely" as it's generated every time the container starts

[node-inspector]: https://nodejs.org/en/docs/guides/debugging-getting-started/

---

* apply awscli/utils/s3-app-bucket*.sh to production App bucket (stagingmms)
    * it was applied to staging environment, but not yet on prod

---

* create a monitoring from App logs for Bandwidth message-failed like the one that follows.

    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059667535Z Bandwidth sms callback [
    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059715316Z   {
    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059722316Z     time: '2022-06-14T18:38:45.798Z',
    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059727236Z     type: 'message-failed',
    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059731996Z     to: '+12408057329',
    [pod/meteor-6b6dd995c8-jmbtc/meteor-worker] 2022-06-14T18:38:46.059736966Z     description: '050003BA0303006F0077 Carrier error 503',

---

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

---

* `FIX` app-build
    * do not dispatch build if one already in place for same version

---

* `FIX` implement a "double check" mechanism for changing DNS uws.t.o domain records
    * the idea is to avoid issues like the one I did changing a production record
    * maybe use an script for Route53 editions which alerts about prod domains or similar
    * try to avoid manual changes (maybe some peer review?)

---

* uwscli auto-setup from main configuration
    * integrate with buildpack deploy scripts

---

* munin: scan cluster ingress domains and add them to the checks (munin-node-clusters)

---

* aws support meeting
    * setup CDN mainly to help saving network transfer costs
    * Route53 app.t.o use geolocation inside US or latency setup
        * versus current weighted 50/50 setup
        * we must keep the "heroku contingency plan" setup or adapt it to new ways

---

* add bot to check we can send emails? (mandrill service)

---

* `CLEAN` /srv/deploy/analysis.git setup for (old) iss72 deploy

---

* `FIX` buildpack:
    * use tag version from command line for publishing the image
    * instead of using the git describe tag
    * currently if a commit has more than one tag associated build fails because previous version already exists
    * that or fix the git describe command to get latest tag instead of first one

    tag invalid: The image tag 'meteor-app-2.64.7-bp21' already exists in the
    'uws' repository and cannot be overwritten because the repository is immutable.

    Publish app version 2.64.8 failed

---

* uwscli:
    * `FIX` non-operator users should not be able to app-restart either
        * app-restart reloads the deploy config, so it can modify the live environment
        * as only operators are allowed to modify the live env: deploy, rollin
        * makes sense also that only them can restart
    * app-build
        * keep a "queued list"
        * only build tag not in "already done list" nor in the "queued list" either
        * to avoid all the duplicate build jobs
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

---

* uwsq: clean failed jobs

---

* `SEC` mongodb credentials rotation schedule

---

* `SEC` aws auth credentials rotation schedule
    * uwsadm and friends "access keys"

---

* mongodb analyzer?

---

* app-autobuild deploy
    * wait some time between deploys on "multi cluster" apps

---

* munin pods_container (check phase)
    "status": {
        "message": "The node was low on resource: memory. Container controller was using 2391212Ki, which exceeds its request of 90Mi. ",
        "phase": "Failed",
        "reason": "Evicted",
        "startTime": "2022-02-09T03:24:23Z"
    }

---

* munin alerts to slack
    * setup/devel bot
    * remove setup munin limit mail alerts
        * dev_ops_vo548nvb
            * munin-alerts TO
            * gmail fetch
            * create forward rules to slack and others

---

* rstudio checks
    * http_loadtime IDE and Jupyter Notebook from jsbatch
    * vm local munin setup (ansible role)

---

* ansible roles
    * monit
        * setup monit to check fail2ban keeps running
        * and others...
    * fail2ban
    * munin

---

* non-prod sites robots.txt to disallow all crawlers?

---

* WAF setup
    * implement fail2ban for kubernets/aws?
    * nginx modsecurity
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/configmap.md#enable-modsecurity
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md#modsecurity

---

* infra docs for internal presentation

---

* k8smon check jobs errors and sendmail.py if any (devel a munin plugin maybe?)
    * aws AMI nodegroup auto upgrade (should be a daily check)

---

* uwscli wish list
    * cleanup old images in ECR
    * app-build
        * we should be able to properly stop/abort a building process
    * show events log or auto-refresh status info
    * control deploy replicas
    * show web proxy logs

---

* cache web assets
    * use separate domain for static assets
    * test meteor appcache

---

* block web access by geoip?
    * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/configmap.md#use-geoip

---

* munin
    * graph app number of active users/sessions

---

* improve web deploys
    * currently it seems that the autoscaler moves around the pods after the deploy so it can re-arrange them in the minimun number of nodes as possible... In that sometimes the nginx-ingress pod is moved around so there's an outage there as the proxy is not available.
    * some ideas:
        * use more than one ingress (maybe in sep namespaces)
        * use different nodegroups for "core" services like nginx and the "main" nodegroup to run our services (web, workers, etc...), using node affinity annotations.
