FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="20210708"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh proftpd-core proftpd-mod-crypto

COPY ./config/ /etc/proftpd/
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh

RUN proftpd --configtest

ENTRYPOINT /usr/local/bin/entrypoint.sh
