# Upgrades schedule

## Cluster

* [aws AMI][aws-ami]
    * `TODO`: 1.19.13-20210914
        * amybeta
        * amy-east
        * amy-west
        * amy-wrkr
    * `2109`: 1.19.13-20210914, 5.4.141
        * uwsdev
        * panoramix
    * 2108: 1.19.6-20210722, 5.4.129
* [k8s/nginx-ingress][nginx-ingress]
    * `TODO`: 0.49.2
    * 2108: 0.45.0 -> 0.48.1
* [k8s/autoscaler][k8s-autoscaler]
    * 1.19.1
* [k8s/cert-manager][cert-manager]
    * `TODO`: 1.3.0 -> 1.5.3
* [k8s/metrics-server][metrics-server]
    * `TODO`: 0.5.0 -> 0.5.1

[aws-ami]: https://docs.aws.amazon.com/eks/latest/userguide/eks-linux-ami-versions.html
[nginx-ingress]: https://github.com/kubernetes/ingress-nginx/releases
[k8s-autoscaler]: https://github.com/kubernetes/autoscaler/releases
[cert-manager]: https://github.com/jetstack/cert-manager/releases
[metrics-server]: https://github.com/kubernetes-sigs/metrics-server/releases

## Debian OS

* jsbatch
    * `2109`: 10 (buster) -> 11 (bullseye)

## Container

* docker/base
    * `2109`: Debian 10 (buster) -> 11 (bullseye)
* docker/base-testing
    * `2109`: Debian bullseye -> bookworm
* docker/golang
    * `2109`: base-testing
* docker/awscli
    * `2109`: amazon/aws-cli
* docker/clamav
    * `2109`: base-testing
* srv/acme
    * `2109`: base-2109
* docker/mkcert
    * `2109`: base-2109
* docker/k8s
    * `2109`: base-2109
* docker/eks
    * `2109`: k8s, eksctl 0.67.0, helm 3.7.0
* docker/uwsbot
    * `2109`: base-2109
* srv/proftpd
    * `2109`: base-2109
* srv/munin
    * `2109`: base-testing, munin-contrib 22ba051
* srv/munin-backend
    * `2109`: munin
* srv/munin-node
    * `2109`: base-testing, munin-contrib 22ba051
* k8s/mon
    * `2109`: k8s, munin, munin-backend, munin-node

## App

### NLP

* docker/base
    * `2109`: Debian 10 (buster) -> 11 (bullseye)

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
