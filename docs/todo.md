# TODO

## Maint

* new Debian (11) stable release (bullseye) - `WIP`
    * upgrade containers: [2109](./infra/upgrades.md)

* productions services - `WIP`
    * [2109](./infra/upgrades.md)
        * upgrades schedule: nginx, autoscaler and such...
        * k8s 1.20 already available (we run 1.19)

## uwscli

* builds cleanup
    * cleanup old images in ECR

* develope webapp
    * users auth/cert manager
    * github webhook
    * jira webhook
    * munin dashboard
    * events history (builds, restarts, deploys, etc...)
    * API for UI interaction

* uwscli integration
    * app-build
        * github webhook integration
        * we should be able to properly stop/abort a building process
    * let Jira know about deployments status
        * https://talkingpointsorg.atlassian.net/jira/software/c/projects/DEV/deployments

* wish list
    * show events log or auto-refresh status info
    * control deploy replicas
    * show web proxy logs
    * uwsq: clean failed jobs

* github CI integration with app builds

## Cluster stats

* web_request.count
    * count_errors_avg: errors average

* resources usage (mem, cpu)
    * nodes
    * pods

* k8s apiserver metrics
    * uwskube get --raw /metrics

## Web

* cache web assets
    * use separate domain for static assets
    * test meteor appcache

### Security

* block access by geoip?

* WAF setup
    * implement fail2ban for kubernets/aws?
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/configmap.md#use-geoip
    * nginx modsecurity
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/configmap.md#enable-modsecurity
        * https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/annotations.md#modsecurity

## Monitoring

* setup munin limit mail alerts
    * uws-bBpwoJrla8TSoefWq8tTPWUJ2VihKADu

* graph app number of active users/sessions
    * set it up on prod

* add munin checks/graphs for NLP

## Cluster

* aws AMI auto-upgrade - `DONE!`
    * setup a cronjob or similar (per cluster) to auto-upgrade AMIs when a new release is available

* custom workers autoscaler
    * scale up every 5 min or so
    * scale down hourly, if needed

* web deploy autoscale setup on custom metrics

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

## Other

* re-design meteor app build to avoid including NLP certs inside container image
    * change buildpack repo app/certs/

* SFTP server for data sharing with schools
    * web integration for user/pass management
    * hook to check/validate uploaded files (try mod_exec)
