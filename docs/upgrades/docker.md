# Docker Upgrades

* `2211` [PR#36](https://github.com/TalkingPts/Infrastructure/pull/36)

---

* [docker/base][debian-container]
    * `2211`: Debian 11.5 (bullseye-20221114-slim)
    * 2203-1: Debian 11.3 (bullseye-20220328-slim)
        * zlib security upgrade CVE-2018-25032
    * 2203: Debian 11.2 (bullseye-20220316-slim)
    * 2109: Debian 10 (buster) -> 11 (bullseye)

[debian-container]: https://hub.docker.com/_/debian

---

* docker/base-testing
    * `2211`: Debian testing (bookworm-20221114-slim)
    * 2203-1: zlib security upgrade CVE-2018-25032
    * 2203: base-2203, Debian bookworm
    * 2109: Debian bullseye -> bookworm

---

* pod/base
    * `2211`: Debian 11.5 (bullseye-20221114-slim)
    * 2203-1: Debian 11.3 (bullseye-20220328-slim)
        * zlib security upgrade CVE-2018-25032
    * 2203: Debian 11.2 (bullseye-20220316-slim)

---

* pod/test
    * `2211`: pod:base
    * 2203: pod:base

---

* docker/golang
    * `2211`: base-2211
        * build.sh: Dockerfile.2211
        * ./docker/upgrades.py -t uws/golang
    * 2203: base-2203
        * build.sh: Dockerfile.2203
        * check.sh: golang-2203
        * cmd.sh: golang-2203
        * devel.sh: golang-2203
        * docs.sh: golang-2203
    * 2109: base-2109

---

* docker/python
    * `2211`: base-2211
        * ./docker/upgrades.py -U docker/python -t uws/python
        * ./docker/upgrades.py -t uws/python
    * 2203: base-2203
    * 2109: base-2109

---

* [docker/awscli][awscli]
    * `2211`: amazon/aws-cli:2.8.12
        * build.sh: Dockerfile.2211
        * ./docker/upgrades.py -t uws/awscli
    * 2203: amazon/aws-cli:2.4.26
    * 2109: amazon/aws-cli

[awscli]: https://hub.docker.com/r/amazon/aws-cli/tags

---

* docker/clamav
    * `2211`: base-testing
        * Dockerfile version
    * 2203: base-testing
    * 2109: base-testing

---

* srv/acme
    * `2211`: base-2211
        * ./docker/upgrades.py -U srv/acme -t uws/acme
        * ./docker/upgrades.py -t uws/acme
    * 2203: base-2203
    * 2109: base-2109

---

* docker/mkcert
    * `2211`: base-2211
        * ./docker/upgrades.py -U docker/mkcert -t uws/mkcert
        * ./docker/upgrades.py -t uws/mkcert
    * 2203: base-2203

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

* docker/asb
    * `2211`: base-2211
        * ./docker/upgrades.py -U docker/asb -t uws/ansible
        * ./docker/upgrades.py -t uws/ansible
    * 2203: base-2203
    * 2109: base-2109

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

* docker/uwscli
    * `2211`: python-2211
        * ./docker/upgrades.py -U docker/uwscli -t uws/cli -s uws/python
        * ./docker/upgrades.py -t uws/cli
    * 2203: python-2203
    * 2109: python-2109

---

* srv/uwsapi
    * `2203`: base-2203

---

* srv/proftpd
    * `2211`: base-2211
        * ./docker/upgrades.py -U srv/proftpd -t uws/proftpd
        * ./docker/upgrades.py -t uws/proftpd
    * 2203: base-2203
    * 2109: base-2109

---

* srv/crond
    * `2211`: mailx-2211
        * ./docker/upgrades.py -U srv/crond -t uws/crond -s uws/mailx
        * ./docker/upgrades.py -t uws/crond
    * 2203: mailx-2203
        * devel.sh: crond-2203
        * run.sh: crond-2203
    * 2109: mailx-2109
        * devel.sh: crond
        * run.sh: crond

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