# Upgrades schedule

## Changelog

* [2203](https://github.com/TalkingPts/Infrastructure/compare/b6a7990e1cae40d194303c7a6375f1d1142d86a9...9b32f1516ff7f6f9eb03149ac1387c3c6c19280f)

## Cluster

* [aws AMI][aws-ami]
    * `2203`: v1.19.15-eks-9c63c4
        * linux 5.4.181-99.354.amzn2.x86_64
        * docker 20.10.7
    * 2109-1: 1.19.14-20211008 (linux 5.4.149, docker 20.10.7)
    * 2109: 1.19.13-20210914, 5.4.141
    * 2108: 1.19.6-20210722, 5.4.129
* [docker/k8s][kubectl]
    * [1.19][kubectl-119]
        * `2203`: 1.19.15/2021-11-10
        * 2109-2: 1.19.15/2021-11-10
        * 2109-1: 1.19.14/2021-10-12
        * 2109: 1.19.13/2021-09-02
* [docker/eks][eksctl], [helm][helm]
    * `2203`: eksctl 0.87.0, helm 3.8.1
    * 2109-1: eksctl 0.76.0, helm 3.7.1
    * 2109: eksctl 0.67.0, helm 3.7.0
* [k8s/nginx-ingress][nginx-ingress]
    * 1.19
        * `2203`: upstream-get.sh 0.49.3
            * all clusters done
        * 2109: 0.49.2
        * 2108: 0.45.0 -> 0.48.1
* [k8s/autoscaler][k8s-autoscaler]
    * 1.19
        * `2203`: upstream-get.sh, setup.sh 1.19.2
            * all clusters done
        * 2109: 1.19.1 -> 1.19.2
* [k8s/cert-manager][cert-manager]
    * `2203`: install.sh 1.7.1
        * all clusters done
    * 2109: 1.3.0 -> 1.5.3
* [k8s/metrics-server][metrics-server]
    * `2203`: upstream-get.sh 0.6.1
        * all clusters done
    * 2109: 0.5.0 -> 0.5.1

[aws-ami]: https://docs.aws.amazon.com/eks/latest/userguide/eks-linux-ami-versions.html
[kubectl]: https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html#linux
[kubectl-119]: https://amazon-eks.s3.us-west-2.amazonaws.com/?versions&prefix=1.19
[eksctl]: https://github.com/weaveworks/eksctl/tags
[helm]: https://github.com/helm/helm/tags
[nginx-ingress]: https://github.com/kubernetes/ingress-nginx/releases
[k8s-autoscaler]: https://github.com/kubernetes/autoscaler/releases
[cert-manager]: https://github.com/jetstack/cert-manager/releases
[metrics-server]: https://github.com/kubernetes-sigs/metrics-server/releases

## Debian OS

* [jsbatch][debian-os]
    * `2203`: 11.2 (bullseye) - 5.10.0-12
    * 2109: 10 (buster) -> 11 (bullseye)
* asb/rstudio
    * `2203`: 11.2 (bullseye) - 5.10.0-12
    * 2109: Debian 11 (bullseye)

[debian-os]: https://www.debian.org/releases/

## Container

* [docker/base][debian-container]
    * `2203`: Debian 11.2 (bullseye-20220316-slim)
    * 2109: Debian 10 (buster) -> 11 (bullseye)
* docker/base-testing
    * `2203`: base-2203, Debian bookworm
    * 2109: Debian bullseye -> bookworm
* pod/base
    * `2203`: Debian 11.2 (bullseye-20220316-slim)
* pod/test
    * `2203`: pod:base
* docker/golang
    * `2203`: base-2203
    * 2109: base-2109
* docker/python
    * `2203`: base-2203
    * 2109: base-2109
* [docker/awscli][awscli]
    * `2203`: amazon/aws-cli:2.4.26
    * 2109: amazon/aws-cli
* docker/clamav
    * `2203`: base-testing
    * 2109: base-testing
* srv/acme
    * `2203`: base-2203
    * 2109: base-2109
* docker/mkcert
    * `2203`: base-2203
* docker/mailx
    * `2203`: base-2203
        * devel.sh: mailx-2203
    * 2109: base-2109
        * devel.sh: mailx
* docker/k8s
    * `2203`: base-2203
    * 2109: base-2109
* docker/k8s:devel
    * `2203`: k8s-2203
* docker/eks
    * `2203`: k8s-2203
    * 2109: k8s
* docker/eks:devel
    * `2203`: eks-2203
* docker/asb
    * `2203`: base-2203
    * 2109: base-2109
* docker/uwsbot
    * `2203`: base-2203, devel golang-2203
    * 2109: base-2109
* docker/uwscli
    * `2203`: python-2203
    * 2109: python-2109
* srv/proftpd
    * `2203`: base-2203
    * 2109: base-2109
* srv/crond
    * `2203`: mailx-2203
        * devel.sh: crond-2203
        * run.sh: crond-2203
    * 2109: mailx-2109
        * devel.sh: crond
        * run.sh: crond
* srv/munin
    * `2203`: base-2203, munin-contrib 438e31f
        * check.sh, utils-devel.sh: python-2203
        * devel.sh, service-start.sh: munin-2203
    * 2109: base-2109, munin-contrib 22ba051
* srv/munin-backend
    * `2203`: munin-2203
        * backend-service-start.sh: munin-backend-2203
    * 2109: munin
* srv/munin-node
    * `2203`: base-2203, munin-contrib 438e31f
        * check.sh, utils-devel.sh: python-2203
        * devel.sh, docker-compose.yml: munin-node-2203
    * 2109: base-2109, munin-contrib 22ba051
* Makefile/utils-publish
    * `2203`: acme-2203
* Makefile/k8smon-publish
    * `2203`: k8s-2203
* Makefile/mon-publish
    * `2203`: munin-2203, munin-backend-2203, munin-node-2203
* Makefile/k8sctl-publish
    * `2203`: eks-k8s-2203
* Makefile/pod-publish
    * `2203`: pod:test

[debian-container]: https://hub.docker.com/_/debian
[awscli]: https://hub.docker.com/r/amazon/aws-cli/tags

## App

### MonitoringBots

* docker
    * `2203`: Debian 11.2 (bullseye-20220316-slim), uwsbot e5cc124
    * 2109: Debian 10 (buster) -> 11 (bullseye), uwsbot 398e147

### NLPService

* docker/base
    * `2203`: Debian 11.2 (bullseye-20220316-slim)
    * 2109: Debian 11 (bullseye)
* src
    * `2203`: base-2203
* sentiment/roberta
    * `2203`: nlpsvc-2203
* sentiment/twitter
    * `2203`: nlpsvc-2203
* Makefile/publish
    * `2203`: nlpsvc-2203, sentiment-twitter-2203
        * `TODO` Schedule with Guillermo a new release date and time.

### Buildpack

* Changelog
    * [2203](https://github.com/TalkingPts/Buildpack/compare/81af1d8b7c139a057a6191d9b6310f43721ca2af...b6f62a5f2aa686ba510123d1768e906d8b2180f8)

* docker/base
    * `2203`: Debian 11.2 (bullseye-20220316-slim)
    * 2109: Debian 10 (buster) -> 11 (bullseye)
* docker/devel
    * `2203`: python-2203
        * build.sh: Dockerfile.2203
* docker/meteor-devel
    * `2203`: base-2203
        * build.sh: Dockerfile.2203
* docker/meteor-1.10.2
    * `2203`: base-2203
        * devel.sh: meteor:1.10.2-2203
        * check/build.sh: Dockerfile.2203
    * 2109: base-2109
* docker/meteor-2.2
    * `2203`: base-2203
        * devel.sh: meteor:2.2-2203
        * check/build.sh: Dockerfile.2203
    * 2109: base-2109
* docker/meteor-2.6
    * `2203`: base-2203
        * devel.sh: meteor:2.6-2203
        * check/build.sh: Dockerfile.2203
* cs
    * `2203`: meteor:2.2-2203
        * build.sh: Dockerfile.2203
        * `TODO` schedule new release with Aram/Gabriel?
    * 2109: meteor-2.2
* app
    * `2203`: meteor-1.10.2-2203
        * build.sh: ${app}/Dockerfile.2203
        * `TODO` schedule new release with Aram/Gabriel?
    * 2109: meteor-1.10.2-2109
* beta
    * `2203`: meteor-1.10.2-2203
    * 2109: meteor-1.10.2-2109
* infra-ui
    * `2203`: meteor-2.6-2203
        * build.sh: Dockerfile.2203
