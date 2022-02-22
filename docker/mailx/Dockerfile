FROM uws/base-2109

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="220222"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh ssl-cert bsd-mailx

RUN adduser uws ssl-cert

RUN install -v -d -o root -g root -m 0750 /srv/etc \
	&& install -v -d -o root -g root -m 0750 /srv/etc/ca \
	&& install -v -d -o root -g root -m 0750 /etc/opt/uws \
	&& install -v -d -o root -g root -m 0750 /etc/opt/uws/ca
