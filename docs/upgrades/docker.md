# Docker Upgrades

* `2309` [PR275][PR275]
* 2305-1 DSA 5417-1: openssl security update - [PR181][PR181]
* 2305 [PR162](https://github.com/TalkingPts/Infrastructure/pull/162)
* 2211 [PR36](https://github.com/TalkingPts/Infrastructure/pull/36)

[PR181]: https://github.com/TalkingPts/Infrastructure/pull/181
[PR275]: https://github.com/TalkingPts/Infrastructure/pull/275

---

* [docker/base][debian-container]
    * `2309`: Debian 12.1 (bookworm-20230919-slim)
        * docker/base/build.sh: base-2309
    * 2305-2: Debian 12.0 (bookworm-20230703-slim)
    * 2305-1 DSA 5417-1: openssl security update
    * 2305: Debian 11.7 (bullseye-20230502-slim)
    * 2211: Debian 11.5 (bullseye-20221114-slim)
    * 2203-1: Debian 11.3 (bullseye-20220328-slim)
    * 2203: Debian 11.2 (bullseye-20220316-slim)
    * 2109: Debian 10 (buster) -> 11 (bullseye)

[debian-container]: https://hub.docker.com/_/debian

---

* docker/base-testing
    * `2309`: Debian testing
        * docker/base-testing/Dockerfile: trixie-20230919-slim
    * 2305-1: Debian testing (trixie-20230703-slim)
    * 2305: Debian testing (bookworm-20230502-slim)
    * 2211: Debian testing (bookworm-20221114-slim)
    * 2203-1: zlib security upgrade CVE-2018-25032
    * 2203: base-2203, Debian bookworm
    * 2109: Debian bullseye -> bookworm

---

* pod/base
    * `2309`: Debian 12.1
        * pod/base/Dockerfile: bookworm-20230919-slim
    * 2305: Debian 11.7 (bullseye-20230502-slim)
    * 2211: Debian 11.5 (bullseye-20221114-slim)
    * 2203-1: Debian 11.3 (bullseye-20220328-slim)
    * 2203: Debian 11.2 (bullseye-20220316-slim)

---

* [docker/awscli][awscli]
    * `2309`: amazon/aws-cli:2.13.21
        * build.sh: awscli-2309
    * 2305: amazon/aws-cli:2.11.20
    * 2211: amazon/aws-cli:2.9.8
    * 2203: amazon/aws-cli:2.4.26
    * 2109: amazon/aws-cli

[awscli]: https://hub.docker.com/r/amazon/aws-cli/tags

---

* docker/base
    * `2309`: Debian 12.1 (bookworm-20230919-slim)
        * docker/VERSION: 230925
        * docker/upgrades.py: from 2305, to 2309, remove 2211

---

* docker/k8s
    * `2309`: ./k8s/upgrades_config.py
        * docker_tag: 2309
        * rm_tags: 2305
    * 2305: ./k8s/upgrades.py
    * 2211: k8s-122-2211
    * 2203: base-2203
    * 2109: base-2109

---

* docker/eks
    * `2309`: ./eks/upgrades.py
        * docker_tag: 2309
        * rm_tags: 2305
    * 2305: ./eks/upgrades.py
    * 2211: base-2211
    * 2203: k8s-2203
    * 2109: k8s

---

    $ make upgrades-check
    $ make upgrades

    # run it again to check "cyclic dependencies"

    $ make upgrades-check
    $ make upgrades

---

    $ make all

---

    $ ./deploy.sh

---

    # as uws@jsbatch

    $ make all
    $ make publish
    $ ./eks/all.sh ./k8s/mon/deploy.sh
