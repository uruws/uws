# TODO

* uwscli integration
    * control meteor services: deploy/restart/rollin - `DONE!`
    * autoscaler logs - `DONE!`
    * web and worker status helper - `DONE!`
    * meteor-build
        * check available disk space before to start a new build
        * cleanup helper
        * github webhook integration

* setup uwscli for amybeta - `DONE!`

* update buildpack to support amybeta uwscli - `DONE!`

* cache web assets
    * setup nginx expire headers

* cluster stats
    * develop munin plugins to graph k8s info
    * nginx stats

* monitoring
    * setup nagios and alerts

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
