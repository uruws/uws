# Upgrades schedule

## Cluster

* aws AMI
    * `2108`: 5.4.129-63.229.amzn2.x86_64
* nginx ingress
    * `2108`: 0.45.0 -> 0.48.1

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
* k8s/mon/k8s
    * `2109`: k8s
* k8s/mon/munin
    * `2109`: munin, munin-backend
* k8s/mon/munin-node
    * `2109`: munin-node

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

### uwsbot

* MonitoringBots/docker
    * `TODO`: Debian 10 (buster) -> 11 (bullseye)
