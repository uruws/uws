# Upgrades schedule

## Debian OS

* jsbatch
    * `2109`: 10 (buster) -> 11 (bullseye)

## Containers

* docker/base
    * `2109`: Debian 10 (buster) -> 11 (bullseye)
* docker/base-testing
    * `2109`: Debian bullseye -> bookworm
* docker/golang
    * `2109`: base-testing
* docker/awscli
    * `2109`
* docker/clamav
    * `2109`: base-testing
* srv/acme
    * `2109`: base-2109
* docker/mkcert
    * `2109`: base-2109
* docker/k8s
    * `2109`: base-2109
* docker/eks
    * `2109`: eksctl 0.67.0, helm 3.7.0
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

## cluster

* aws AMI
    * `2108`
* nginx ingress
    * `2108`: 0.45.0 -> 0.48.1
