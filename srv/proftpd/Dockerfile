FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="20210708"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh proftpd-core proftpd-mod-crypto

COPY ./secret/ssh/ /etc/ssh/
RUN chmod -v 0600 /etc/ssh/ssh_host_*_key \
	&& chmod -v 0640 /etc/ssh/ssh_host_*_key.pub

COPY ./config/ /etc/proftpd/
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh

RUN proftpd --configtest

ENTRYPOINT /usr/local/bin/entrypoint.sh
