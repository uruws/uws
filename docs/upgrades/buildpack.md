# Buildpack pgrades schedule

* Changelog
    * [2203](https://github.com/TalkingPts/Buildpack/compare/81af1d8b7c139a057a6191d9b6310f43721ca2af...b6f62a5f2aa686ba510123d1768e906d8b2180f8)

* docker/base
    * `2211`: Debian 11.5 (bullseye-20221205-slim)
    * 2203-1: Debian 11.3 (bullseye-20220328-slim)
        * zlib security upgrade CVE-2018-25032
    * 2203: Debian 11.2 (bullseye-20220316-slim)
    * 2109: Debian 10 (buster) -> 11 (bullseye)
* docker/devel
    * `2211`:
        * uws/docker/upgrades.py -U docker/devel -t uws/buildpack:devel -s uws/python
        * uws/docker/upgrades.py -t uws/buildpack:devel
    * 2203: python-2203
        * build.sh: Dockerfile.2203
* docker/meteor
    * `2211`:
        * uws/docker/upgrades.py -U docker/meteor -t uws/meteor -s uws/buildpack:base
        * uws/docker/upgrades.py -t uws/meteor
    * 2203: base-2203, meteor release 2.7.1
        * build.sh: Dockerfile.2203
        * check/star/.meteor/release: METEOR@2.7.1
        * devel.sh: meteor-2203
* docker/meteor-devel
    * `2211`:
        * uws/docker/upgrades.py -U docker/meteor-devel -t uws/meteor:devel -s uws/meteor
        * uws/docker/upgrades.py -t uws/meteor:devel
    * 2203: meteor-2203
        * build.sh: Dockerfile.2203
* deploy
    * `2203`: Dockerfile buildpack:base-2203
* cs
    * `2203`: meteor:2.2-2203
        * build.sh: Dockerfile.2203
    * 2109: meteor-2.2
* app
    * `2203`: meteor-1.10.2-2203
        * build.sh: ${app}/Dockerfile.2203
    * 2109: meteor-1.10.2-2109
* beta
    * `2203`: meteor-1.10.2-2203
    * 2109: meteor-1.10.2-2109
* infra-ui
    * `2203`: meteor-2203
        * build.sh: Dockerfile.2203
