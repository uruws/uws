* setup worker-test env - `DONE!`

* upgrade jsbatch resources - `DONE!`
    * t3a.large to t3a.xlarge

* userInbox.jobs limits - `DONE!`
    * warning:  3s -> 7s
    * critical: 7s -> 9s

* setup Mauro for Infra-UI development - `DONE!`

* `FIX` mongodb app prod and staging "engine checks" - `DONE!`
    * it stopped working after mongo credentials rotation

* `FIX` CS test cluster setup - `DONE!`
    * heroku stopped working... we need an aws setup for it

* munin: mongo checks and bots use secondary servers - `DONE!`

* `URGENT` cluster stack
    * k8s 1.20 (and 1.21) already available (we run 1.19)
    * Amazon EKS has deprecated Kubernetes version 1.19 and this version will no
      longer be supported as of June 30, 2022. As of June 30, 2022, you will no
      longer be able to create new 1.19 clusters and all EKS clusters running
      Kubernetes version 1.19 will be updated to the latest available platform
      version of Kubernetes version 1.20.

* infra-api - `WIP`
    * devel and setup

* [DEV-2473](https://talkingpointsorg.atlassian.net/browse/DEV-2473) - SOC2 fixes/setup
    * DEV-2475 - Unrestricted File Upload - `WIP`
        * `NOTE` I think a better setup could be that App sends assets to S3 but
          we serve does assests from a CDN created for that purpose. That way we
          avoid some S3 cost and we only pay for CDN uploading.
        * create script to set S3 policies so we restrict upload file types
    * DEV-2478, DEV-2482 - 3rd party cookies
        * investigate if there's something we can do there at web server level
    * DEV-2484 - HTTP Secure headers implementation
        * we had it on this TODO already as: nginx secure headers

* nginx secure headers
    * CSP
        * https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
        * once aws.testing is done try/deploy there

* AI-Backend (Angel) S3 bucket for DB dumps

* `FIX` implement a "double check" mechanism for changing DNS uws.t.o domain records
    * the idea is to avoid issues like the one I did changing a production record
    * maybe use an script for Route53 editions which alerts about prod domains or similar
    * try to avoid manual changes (maybe some peer review?)

* `FIX` app-build
    * do not dispatch build if one already in place for same version
    * avoid the build cleanup on each run, schedule it to run once a day or similar (per app)

* uwscli auto-setup from main configuration
    * integrate with buildpack deploy scripts

* munin: scan cluster ingress domains and add them to the checks (munin-node-clusters)

* aws support meeting
    * setup CDN mainly to help saving network transfer costs
    * Route53 app.t.o use geolocation inside US or latency setup
        * versus current weighted 50/50 setup
        * we must keep the "heroku contingency plan" setup or adapt it to new ways
    * EKS ec2 "reserved instances" setup to help saving costs

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

* k8sctl: deprecate?

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

* cs runs on amybeta cluster: move it?
    * make it the first k8s v1.21 version?

* App meteor upgrade
    * take the opportunity to start using docker setup?

* nlpsvc: separate apps namespaces (for graphs and cli status/logs)

* munin
    * add pod/test to mon deploys and check it from jsbatch munin cluster checks

* configurable app-autoscale

* configurable app-autobuild

* check clusters k8s mon and ctl internal services from jsbatch/ops.uws

* golang tools unittests and CI integration
    * golib
    * uwsbot
    * uwsbot-stats
    * api-job-stats

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

* develope infra webapp
    * users auth/cert manager
    * github webhook
    * jira webhook
    * munin dashboard
    * events history (builds, restarts, deploys, etc...)
    * API for UI interaction

* infra docs for internal presentation

* `FIX` k8smon: munin-alerts volume setup
    * until we can fix the volumes claim config, we could use one of the already existent volumes and set ALERTS_QDIR to point to it

* k8smon check jobs errors and sendmail.py if any (devel a munin plugin maybe?)
    * aws AMI nodegroup auto upgrade (should be a daily check)

* uwscli integration
    * cleanup old images in ECR
    * app-build
        * github webhook integration
        * we should be able to properly stop/abort a building process
    * let Jira know about deployments status
        * https://talkingpointsorg.atlassian.net/jira/software/c/projects/DEV/deployments
    * github CI/Actions integration with app builds

* uwscli wish list
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
        * set it up on prod

* web deploy autoscale setup on custom metrics

* web and workers scheduled (uwscli crontab) scale up/down
    * restart services before (1h) scale up

* web /bandwidthCallbackSms requests
    * add bot check/graph

* nginx
    * split cluster load over N instances instead of only 1
    * run them in their own node group?
    * or tune mem and cpu resources to make them run in a "dedicated" node?

* improve web deploys
    * currently it seems that the autoscaler moves around the pods after the deploy so it can re-arrange them in the minimun number of nodes as possible... In that sometimes the nginx-ingress pod is moved around so there's an outage there as the proxy is not available.
    * some ideas:
        * use more than one ingress (maybe in sep namespaces)
        * use different nodegroups for "core" services like nginx and the "main" nodegroup to run our services (web, workers, etc...), using node affinity annotations.
