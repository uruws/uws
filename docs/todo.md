# TODO

* setup munin limit mail alerts - `WIP`
    * jsbatch smtps with tls auth relay service - `DONE!`
    * sendmail.py lib to send emails via smtps relay - `DONE!`
    * clusters smtps setup - `DONE!`
    * remove uws-bBpwoJrla8TSoefWq8tTPWUJ2VihKADu
    * create new "alerts" account
        * create forward rules to slack and others

* setup Rina OUSD VM
    * AWS Workspaces
        * https://sa-east-1.console.aws.amazon.com/workspaces/home
    * Setup RStudio server
        * https://www.rstudio.com/products/rstudio/#rstudio-server
        https://www.r-project.org/
        * server access.
            * HTTPS only?
            * VNC or RDP desktop otherwise
    * N. California location
    * Data storage
        * LVM encrypted volumes?
        * with backups (snapshots?)
        * group based storage dirs access

* new Debian (11) stable release (bullseye) - `DONE!`
    * upgrade containers: [2109](./infra/upgrades.md)

* aws AMI auto-upgrade - `DONE!`
    * setup a cronjob or similar (per cluster) to auto-upgrade AMIs when a new release is available

* cluster services - `DONE!`
    * [2109](./infra/upgrades.md)
        * upgrades schedule: nginx, autoscaler and such...
        * `FAIL`: cluster autoscaler failed to upgrade on all clusters but uwsdev

* cluster stack
    * k8s 1.20 (and 1.21) already available (we run 1.19)

* cluster stats
    * web_request.count
        * count_errors_avg: errors average
    * resources usage (mem, cpu)
        * nodes
        * pods
    * k8s apiserver metrics
        * uwskube get --raw /metrics

* munin alerts: tune/add graph limits
    * all cluster checks
    * uwsbots limits

* k8smon check jobs errors and sendmail.py if any (devel a munin plugin maybe?)
    * aws AMI nodegroup auto upgrade (should be a daily check)

* develope infra webapp
    * users auth/cert manager
    * github webhook
    * jira webhook
    * munin dashboard
    * events history (builds, restarts, deploys, etc...)
    * API for UI interaction

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

* WAF setup
    * implement fail2ban for kubernets/aws?
    * nginx modsecurity
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/configmap.md#enable-modsecurity
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md#modsecurity

* munin
    * graph app number of active users/sessions
        * set it up on prod
    * add checks/graphs for NLP

* custom workers autoscaler
    * scale up every 5 min or so
    * scale down hourly, if needed

* web deploy autoscale setup on custom metrics

* web and workers scheduled (uwscli crontab) scale up/down
    * restart services before (1h) scale up

* web /bandwidthCallbackSms requests
    * add bot check/graph
    * remove setup from workers cluster?

* setup amy staging cluster

* split nginx cluster proxy load over N instances instead of only 1

* improve web deploys
    * currently it seems that the autoscaler moves around the pods after the deploy so it can re-arrange them in the minimun number of nodes as possible... In that sometimes the nginx-ingress pod is moved around so there's an outage there as the proxy is not available.
    * some ideas:
        * use more than one ingress (maybe in sep namespaces)
        * use different nodegroups for "core" services like nginx and the "main" nodegroup to run our services (web, workers, etc...), using node affinity annotations.

* re-design meteor app build to avoid including NLP certs inside container image
    * change buildpack repo app/certs/

* SFTP server for data sharing with schools
    * web integration for user/pass management
    * hook to check/validate uploaded files (try mod_exec)
