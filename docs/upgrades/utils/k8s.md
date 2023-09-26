# Kubernetes Utils Upgrades

* ./k8s/utils.json
    * [autoscaler](https://github.com/kubernetes/autoscaler/tags)
    * [helm](https://github.com/helm/helm/tags)
    * [kubectl](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)
    * [kubeshark](https://github.com/kubeshark/kubeshark/releases)

* ./eks/utils.json
    * [eksctl](https://github.com/eksctl-io/eksctl/tags)

    $ make upgrades

# Still Missing

* [k8s/nginx-ingress][nginx-ingress]
    * 1.22
        * `2203`: upstream-get.sh 1.2.1
    * 1.19
        * 2203: upstream-get.sh 0.49.3
            * all clusters done
        * 2109: 0.49.2
        * 2108: 0.45.0 -> 0.48.1

[nginx-ingress]: https://github.com/kubernetes/ingress-nginx/releases

---

* [k8s/cert-manager][cert-manager]
    * `2203`: install.sh 1.8.1
        * all clusters done
    * 2109: 1.3.0 -> 1.5.3

[cert-manager]: https://github.com/jetstack/cert-manager/releases

---

* [k8s/metrics-server][metrics-server]
    * `2309`: 0.6.4
        * ./k8s/metrics-server/upstream-get.sh
    * 2203: upstream-get.sh 0.6.1
    * 2109: 0.5.0 -> 0.5.1

[metrics-server]: https://github.com/kubernetes-sigs/metrics-server/releases
