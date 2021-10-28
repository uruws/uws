# TODO

* rstudio (Rina)
    * setup jupyter (notebook and lab)
        * https://jupyter.org/

* munin alerts: tune/add graph limits
    * all cluster checks
        * nodes_condition - `DONE!`
            * Disk, Mem and PID Pressure
        * pod_container (all? | per pod)
            * failed (ratio?)
            * restart ratio
        * web_request (response?)
            * errors_ratio (once created)
        * web_latency?
        * web_ssl - `DONE!`
            * cert expire
        * web_time
            * response (request?) avg
    * jsbatch - `DONE!`
        * load avg
        * uptime
    * app.t.o
        * apijob - `DONE!`
            * make failed jobs a DERIVE graph and set limits there
            * elapsed_time
            * queue limits
                * cleverSynch
                * firebase
                * messages
        * mongo lag - `DONE!`
        * uwsbot - `DONE!`
            * set alerts on index graph

* setup munin limit mail alerts - `DONE!`
    * setup dev_ops_vo548nvb
        * munin-alerts TO
        * gmail fetch
        * create forward rules to slack and others

* ansible roles - `WIP`
    * fail2ban
    * munin

* WAF setup
    * implement fail2ban for kubernets/aws?
    * nginx modsecurity
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/configmap.md#enable-modsecurity
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md#modsecurity

* infra app
    * auth service

* k8s/ctl - `FIX`: munin-alerts volume setup
    * until we can fix the volumes claim config, we could use one of the already existent volumes and set ALERTS_QDIR to point to it

* monit
    * setup monit to check fail2ban keeps running
    * and others...

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
