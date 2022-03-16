# Upgrades schedule

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
    * `2109`: 0.49.2
    * 2108: 0.45.0 -> 0.48.1
* [k8s/autoscaler][k8s-autoscaler]
    * 1.19
        * `TODO`: 1.19.1 -> 1.19.2
            * amybeta
            * amy-wrkr
            * amy-east
            * amy-west
            * panoramix
                * 1.19.2 fails
        * `2109`: 1.19.1 -> 1.19.2
            * uwsdev
* [k8s/cert-manager][cert-manager]
    * `2109`: 1.3.0 -> 1.5.3
* [k8s/metrics-server][metrics-server]
    * `2109`: 0.5.0 -> 0.5.1

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
    * `2203`: 11 (bullseye) - 5.10.0-12
    * 2109: 10 (buster) -> 11 (bullseye)
* asb/rstudio
    * `2109`: Debian 11 (bullseye)

[debian-os]: https://www.debian.org/releases/

## Container

* [docker/base][debian-container]
    * `2203`: Debian 11 (bullseye)
    * 2109: Debian 10 (buster) -> 11 (bullseye)
* docker/base-testing
    * `2203`: base-2203, Debian bookworm
    * 2109: Debian bullseye -> bookworm
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
    * 2109: base-2109
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
    * `2109`: base-2109
* docker/uwscli
    * `2109`: python-2109
* srv/proftpd
    * `2109`: base-2109
* srv/munin
    * `2109`: base-2109, munin-contrib 22ba051
* srv/munin-backend
    * `2109`: munin
* srv/munin-node
    * `2109`: base-2109, munin-contrib 22ba051
* k8s/mon
    * `2109`: k8s, munin, munin-backend, munin-node
* k8s/ctl
    * `2109`: eks

[debian-container]: https://hub.docker.com/_/debian
[awscli]: https://hub.docker.com/r/amazon/aws-cli/tags

## App

### NLPService

* docker/base
    * `2109`: Debian 11 (bullseye)

### Buildpack

* docker/base
    * `2109`: Debian 10 (buster) -> 11 (bullseye)
* docker/meteor-2.2
    * `2109`: base-2109
* cs
    * `2109`: meteor-2.2
* docker/meteor-1.10.2
    * `2109`: base-2109
* beta
    * `2109`: meteor-1.10.2-2109
* app
    * `2109`: meteor-1.10.2-2109

### MonitoringBots

* docker
    * `2109`: Debian 10 (buster) -> 11 (bullseye), uwsbot 398e147
