* uwscli - `DONE!`
    * `FIX` autobuild deploys
        * 2.62.5 successfully auto built and auto deployed to test cluster
    * app access by group

* workers - `DONE!`
    * remove web endpoint (worker.uws.talkingpts.org)
        * check traffic first

* 2202 round of [upgrades](./infra/upgrades.md) - `WIP`
    * fix munin pod failed ratio when running == 0 and failed > 0
    * fix munin pod state Error not being counted for failed pods?
    * fix aws-ami auto upgrades (k8s/ctl)

* nlp app-deploy access

* uwscli:
    * cli/buildpack.sh should manage the log and email report if any fail
    * cli/app-build.sh should do the same

* uwsq: clean failed jobs

* mongodb credentials rotation?

* mongodb analyzer?

* app-autobuild deploy
    * wait some time between deploys on "multi cluster" apps

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

* munin: add pod/test to mon deploys and check it from jsbatch munin cluster checks

* configurable app-autoscale

* configurable app-autobuild

* check clusters k8s mon and ctl internal services from jsbatch/ops.uws

* golang tools unittests and CI integration
    * golib
    * uwsbot
    * uwsbot-stats
    * api-job-stats

* nginx secure headers
    * CSP
        * https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
        * once aws.testing is done try/deploy there

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

* `FIX`: k8s/ctl - munin-alerts volume setup
    * until we can fix the volumes claim config, we could use one of the already existent volumes and set ALERTS_QDIR to point to it

* cluster stack
    * k8s 1.20 (and 1.21) already available (we run 1.19)

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
