# Docker Upgrades

* `2305` [PR162](https://github.com/TalkingPts/Infrastructure/pull/162)
* 2211 [PR36](https://github.com/TalkingPts/Infrastructure/pull/36)

---

* [docker/base][debian-container]
    * `2305`: Debian 11.7 (bullseye-20230502-slim)
    * 2211: Debian 11.5 (bullseye-20221114-slim)
    * 2203-1: Debian 11.3 (bullseye-20220328-slim)
        * zlib security upgrade CVE-2018-25032
    * 2203: Debian 11.2 (bullseye-20220316-slim)
    * 2109: Debian 10 (buster) -> 11 (bullseye)

[debian-container]: https://hub.docker.com/_/debian

---

* docker/base-testing
    * `2305`: Debian testing (bookworm-20230502-slim)
    * 2211: Debian testing (bookworm-20221114-slim)
    * 2203-1: zlib security upgrade CVE-2018-25032
    * 2203: base-2203, Debian bookworm
    * 2109: Debian bullseye -> bookworm

---

* pod/base
    * `2305`: Debian 11.7 (bullseye-20230502-slim)
    * 2211: Debian 11.5 (bullseye-20221114-slim)
    * 2203-1: Debian 11.3 (bullseye-20220328-slim)
        * zlib security upgrade CVE-2018-25032
    * 2203: Debian 11.2 (bullseye-20220316-slim)

---

* pod/test
    * `2305`: pod:base
    * 2211: pod:base
    * 2203: pod:base

---

* [docker/awscli][awscli]
    * `2305`: amazon/aws-cli:2.11.20
        * build.sh: Dockerfile.2211
    * 2211: amazon/aws-cli:2.9.8
        * build.sh: Dockerfile.2211
        * ./docker/upgrades.py -t uws/awscli
    * 2203: amazon/aws-cli:2.4.26
    * 2109: amazon/aws-cli

[awscli]: https://hub.docker.com/r/amazon/aws-cli/tags

---

* docker/mailx
    * `2211`: base-2211
        * ./docker/upgrades.py -U docker/mailx -t uws/mailx
        * ./docker/upgrades.py -t uws/mailx
    * 2203: base-2203
        * devel.sh: mailx-2203
    * 2109: base-2109
        * devel.sh: mailx

---

* docker/k8s
    * `2211`: k8s-122-2211
        * ./docker/upgrades.py -U docker/k8s/122 -t uws/k8s-122
        * ./docker/upgrades.py -t uws/k8s-122
        * ./docker/upgrades.py -t 'uws/${K8S_IMAGE}'
    * 2203: base-2203
    * 2109: base-2109

---

* docker/eks
    * `2211`: base-2211
        * ./docker/upgrades.py -U docker/eks/122 -t uws/eks-122 -s uws/k8s-122
        * ./docker/upgrades.py -t uws/eks-122
        * ./docker/upgrades.py -t 'uws/${EKS_IMAGE}'
    * 2203: k8s-2203
    * 2109: k8s

---

* docker/uwsbot
    * `2211`: base-2211
        * ./docker/upgrades.py -U docker/uwsbot -t uws/uwsbot
        * ./docker/upgrades.py -t uws/uwsbot
    * 2203: base-2203
        * devel.sh: golang-2203
    * 2109: base-2109

---

* docker/heroku
    * `2211`: Dockerfile

---

* docker/uwscli
    * `2211`: python-2211
        * ./docker/upgrades.py -U docker/uwscli -t uws/cli -s uws/python
        * ./docker/upgrades.py -t uws/cli
    * 2203: python-2203
    * 2109: python-2109

---

* srv/proftpd
    * `2211`: base-2211
        * ./docker/upgrades.py -U srv/proftpd -t uws/proftpd
        * ./docker/upgrades.py -t uws/proftpd
    * 2203: base-2203
    * 2109: base-2109

---

* srv/munin
    * `2211`: base-2211
        * ./docker/upgrades.py -U srv/munin -t uws/munin
        * ./docker/upgrades.py -t uws/munin
    * 2203: base-2203, munin-contrib 438e31f
        * check.sh, utils-devel.sh: python-2203
        * devel.sh, service-start.sh: munin-2203
    * 2109: base-2109, munin-contrib 22ba051

---

* srv/munin-backend
    * `2211`: munin-2211
        * ./docker/upgrades.py -U srv/munin-backend -t uws/munin-backend -s uws/munin
        * ./docker/upgrades.py -t uws/munin-backend
    * 2203: munin-2203
        * backend-service-start.sh: munin-backend-2203
    * 2109: munin

---

* srv/munin-node
    * `2211`: base-2211
        * ./docker/upgrades.py -U srv/munin-node -t uws/munin-node
        * ./docker/upgrades.py -t uws/munin-node
    * 2203: base-2203, munin-contrib 438e31f
        * check.sh, utils-devel.sh: python-2203
        * devel.sh, docker-compose.yml: munin-node-2203
        * host/assets/jsbatch/uws/init/35-munin-node-service: munin-node-2203
    * 2109: base-2109, munin-contrib 22ba051

---

* srv/herokud
    * `2211`: crond-2211
        * ./docker/upgrades.py -U srv/herokud -t uws/herokud -s uws/crond
        * ./docker/upgrades.py -t uws/herokud
