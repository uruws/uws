# TODO

* meteor test - https://talkingpointsorg.atlassian.net/browse/DEV-441
    * buildpack integration
        * https://guide.meteor.com/testing.html
    * meteor-build integration
        * based on official docs we could do: test, build, install, deploy

* uwscli integration
    * meteor-build
        * github webhook integration
        * check available disk space before to start a new build
        * cleanup helper

* setup amy staging cluster

* cache web assets
    * setup nginx expire headers

* cluster stats
    * develop munin plugins to graph k8s info
    * nginx stats

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
