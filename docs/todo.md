# TODO

* nlpsvc new setup - `DONE!`
    * sentiment-roberta
    * topic-automl

* k8s and eks utils [upgrade][upgrades] - `DONE!`
    * k8s `2109-2`
    * eks `2109-1`

[upgrades]: https://github.com/TalkingPts/Infrastructure/blob/master/docs/infra/upgrades.md

* setup tapo.testing cluster - `WIP`
    * as similar as possible to the prod setup
    * [app-test-1](https://amy-test-1.uws.talkingpts.org/munin/)
    * [app-test-2](https://amy-test-2.uws.talkingpts.org/munin/)

* check ev15min new tags on App repo - `WIP`
    * build and deploy to tapo.testing

* k8s and eks CI checks - `DONE!`

* uwscli app access by group

* nginx secure headers
    * CSP
        * https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
        * once aws.testing is done try/deploy there

* munin alerts to slack
    * setup/devel bot
    * remove setup munin limit mail alerts
        * dev_ops_vo548nvb
            * munin-alerts TO
            * gmail fetch
            * create forward rules to slack and others

* munin alerts: tune/add graph limits
    * all cluster checks
        * web_request (response?)
            * errors_ratio (once created)
        * web_latency?
        * web_time
            * response (request?) avg

* rstudio checks
    * http_loadtime IDE and Jupyter Notebook from jsbatch
    * vm local munin setup (ansible role)

* ansible roles
    * monit
        * setup monit to check fail2ban keeps running
        * and others...
    * fail2ban
    * munin

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

* k8s/ctl - `FIX`: munin-alerts volume setup
    * until we can fix the volumes claim config, we could use one of the already existent volumes and set ALERTS_QDIR to point to it

* cluster stack
    * k8s 1.20 (and 1.21) already available (we run 1.19)

* cluster stats
    * web_request.count
        * count_per_minute
        * count_errors_avg: errors average
    * resources usage (mem, cpu)
        * nodes
        * pods
    * k8s apiserver metrics
        * uwskube get --raw /metrics

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
    * uwsq: clean failed jobs

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
    * remove setup from workers cluster?

* split nginx cluster proxy load over N instances instead of only 1

* improve web deploys
    * currently it seems that the autoscaler moves around the pods after the deploy so it can re-arrange them in the minimun number of nodes as possible... In that sometimes the nginx-ingress pod is moved around so there's an outage there as the proxy is not available.
    * some ideas:
        * use more than one ingress (maybe in sep namespaces)
        * use different nodegroups for "core" services like nginx and the "main" nodegroup to run our services (web, workers, etc...), using node affinity annotations.

* SFTP server for data sharing with schools
    * web integration for user/pass management
    * hook to check/validate uploaded files (try mod_exec)
