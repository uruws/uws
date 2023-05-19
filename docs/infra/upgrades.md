# Infra Upgrades

* [Server](../docs/upgrades/server.md)
* [Docker](../docs/upgrades/docker.md)

## Changelog

* `2305` [M12](https://github.com/TalkingPts/Infrastructure/milestone/12)

## Cluster

* [aws AMI][aws-ami]
    * `2211`: ./eks/admin-all.sh k8s/nodes/upgrade.sh
    * 2203: v1.19.15-eks-9c63c4
        * linux 5.4.181-99.354.amzn2.x86_64
        * docker 20.10.7
    * 2109-1: 1.19.14-20211008 (linux 5.4.149, docker 20.10.7)
    * 2109: 1.19.13-20210914, 5.4.141
    * 2108: 1.19.6-20210722, 5.4.129
* [docker/k8s][kubectl]
    * [1.25][kubectl-125]
        * `2211`: kubectl 1.25.5/2023-01-11, helm 3.11.0
    * [1.22][kubectl-122]
        * 2203: 1.22.6/2022-03-09
    * [1.19][kubectl-119]
        * 2203: 1.19.15/2021-11-10
        * 2109-2: 1.19.15/2021-11-10
        * 2109-1: 1.19.14/2021-10-12
        * 2109: 1.19.13/2021-09-02
* [docker/eks][eksctl], [helm][helm]
    * 1.25
        * `2203`: eksctl 0.126.0
    * 1.22
        * 2203: eksctl 0.101.0, helm 3.9.0
    * 1.19
        * 2203: eksctl 0.87.0, helm 3.8.1
        * 2109-1: eksctl 0.76.0, helm 3.7.1
        * 2109: eksctl 0.67.0, helm 3.7.0
* [k8s/nginx-ingress][nginx-ingress]
    * 1.22
        * `2203`: upstream-get.sh 1.2.1
    * 1.19
        * 2203: upstream-get.sh 0.49.3
            * all clusters done
        * 2109: 0.49.2
        * 2108: 0.45.0 -> 0.48.1
* [k8s/autoscaler][k8s-autoscaler]
    * 1.25
        * `2211`: upstream-get.sh, 1.25/deploy.yaml 1.25.0
    * 1.22
        * 2203: upstream-get.sh, 1.22/deploy.yaml 1.22.2
    * 1.19
        * 2203: upstream-get.sh, setup.sh 1.19.2
            * all clusters done
        * 2109: 1.19.1 -> 1.19.2
* [k8s/cert-manager][cert-manager]
    * `2203`: install.sh 1.8.1
        * all clusters done
    * 2109: 1.3.0 -> 1.5.3
* [k8s/metrics-server][metrics-server]
    * `2203`: upstream-get.sh 0.6.1
        * all clusters done
    * 2109: 0.5.0 -> 0.5.1

[aws-ami]: https://docs.aws.amazon.com/eks/latest/userguide/eks-linux-ami-versions.html
[kubectl]: https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html#linux
[kubectl-119]: https://amazon-eks.s3.us-west-2.amazonaws.com/?versions&prefix=1.19
[kubectl-122]: https://amazon-eks.s3.us-west-2.amazonaws.com/?versions&prefix=1.22
[eksctl]: https://github.com/weaveworks/eksctl/tags
[helm]: https://github.com/helm/helm/tags
[nginx-ingress]: https://github.com/kubernetes/ingress-nginx/releases
[k8s-autoscaler]: https://github.com/kubernetes/autoscaler/releases
[cert-manager]: https://github.com/jetstack/cert-manager/releases
[metrics-server]: https://github.com/kubernetes-sigs/metrics-server/releases

## App

### MonitoringBots

* Changelog

    * [2203](https://github.com/TalkingPts/MonitoringBots/compare/ff20e4dac62f53d2cddd4399e820f2fe781604c1...0006eb83ef048c00418c8e5727faf977e8d25b01)

* docker
    * `2203-1`: Debian 11.3 (bullseye-20220328-slim)
        * zlib security upgrade CVE-2018-25032
    * 2203: Debian 11.2 (bullseye-20220316-slim), uwsbot e5cc124
    * 2109: Debian 10 (buster) -> 11 (bullseye), uwsbot 398e147

### OfflinePage

* Dockerfile
    * `2211`: base-2211
* docker/devel/Dockerfile
    * `2211`: golang-2211
