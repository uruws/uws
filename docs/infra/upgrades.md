# Upgrades schedule

* Debian OS
    * jsbatch
        * `2109`: 10 (buster) -> 11 (bullseye)

* containers
    * docker/base
        * `2109`: Debian 10 (buster) -> 11 (bullseye)
    * docker/base-testing
        * `2109`: Debian bullseye -> bookworm
    * docker/golang
        * `2109`: base-testing
    * docker/mkcert
        * `2109`: base-2109

* external utils
    * docker/awscli
        * `2109`
    * docker/clamav
        * `2109`: base-testing
    * srv/acme
        * `2109`: base-2109

* cluster
    * aws AMI
        * `2108`
    * nginx ingress
        * `2108`: 0.45.0 -> 0.48.1
