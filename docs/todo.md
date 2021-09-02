# TODO

* cache web assets
    * use separate domain for static assets
    * test meteor appcache

* cluster stats - `WIP`
    * develop munin plugins to graph k8s info
    * nginx stats

* uwscli
    * remove app-build --no-test - `DONE!`
    * grant access for developers using personal users
    * limit app-deploy and app-rollin usage for "admins" only

* setup munin limit mail alerts
    * uws-bBpwoJrla8TSoefWq8tTPWUJ2VihKADu

* new Debian (11) stable release (bullseye)
    * upgrade containers

* graph app number of active users/sessions
    * set it up on prod

* custom workers autoscaler
    * scale up every 5 min or so
    * scale down hourly, if needed

* web deploy autoscale setup on custom metrics

* web /bandwidthCallbackSms requests
    * add bot check/graph

* uwscli integration
    * docker images cleanup
    * app-build
        * github webhook integration
        * we should be able to properly stop/abort a building process
    * devel API for UI interaction
    * let Jira know about deployments status
        * https://talkingpointsorg.atlassian.net/jira/software/c/projects/DEV/deployments
    * show events log or auto-refresh status info
    * control deploy replicas
    * show web proxy logs
    * uwsq: clean failed jobs

* setup amy staging cluster

* add munin checks/graphs for NLP

* split nginx cluster proxy load over N instances instead of only 1

* improve web deploys
    * currently it seems that the autoscaler moves around the pods after the deploy so it can re-arrange them in the minimun number of nodes as possible... In that sometimes the nginx-ingress pod is moved around so there's an outage there as the proxy is not available.
    * some ideas:
        * use more than one ingress (maybe in sep namespaces)
        * use different nodegroups for "core" services like nginx and the "main" nodegroup to run our services (web, workers, etc...), using node affinity annotations.

* productions services maintenance
    * upgrades schedule: nginx, autoscaler and such...
    * k8s 1.20 already available (we run 1.19)

* re-design meteor app build to avoid including NLP certs inside container image
    * change buildpack repo app/certs/

* SFTP server for data sharing with schools
    * web integration for user/pass management
    * hook to check/validate uploaded files (try mod_exec)
