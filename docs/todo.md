# TODO

* Security
    * docs about Mac and Windows hard disk encryption

* buildpack internal tests  - `DONE!`

* crowdsourcing setup
    * buildpack setup - `DONE!`
    * deploy on beta cluster
    * uwscli build/deploy/status - `DONE!`

* worker job stats
    * add graph for waiting status
        * it needs to be configurable per job

* graph app number of active users/sessions
    * count mongo activeSessions collection (once it gets to prod)

* custom workers autoscaler
    * scale up every 5 min or so
    * scale down hourly, if needed

* SFTP server for data sharing with schools
    * web integration for user/pass management
    * hook to check/validate uploaded files (try mod_exec)

* re-implement uwscli tools in python to avoid code duplication, improve args parsing and such...

* uwscli integration
    * meteor-build
        * github webhook integration
        * check available disk space before to start a new build
        * cleanup helper
        * we should be able to properly stop/abort a building process
    * devel API for UI interaction
    * let Jira know about deployments status
        * https://talkingpointsorg.atlassian.net/jira/software/c/projects/DEV/deployments
    * show events log or auto-refresh status info
    * check deploy tag already exists (*-deploy scripts)
    * control deploy replicas?

* setup amy staging cluster

* cache web assets
    * setup nginx expire headers

* cluster stats
    * develop munin plugins to graph k8s info
    * nginx stats

* web deploy autoscale setup on custom metrics

* monitoring
    * setup nagios and alerts

* add munin checks/graphs for NLP

* uwscli
    * uwsq: clean failed jobs

* internal CA

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
