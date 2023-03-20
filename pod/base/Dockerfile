FROM debian:bullseye-20221114-slim

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="230208"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ADD ./utils/apt-*.sh /root/bin/
RUN chmod -v 0750 /root/bin /root/bin/*.sh

RUN /root/bin/apt-distupgrade.sh
RUN /root/bin/apt-install.sh bash ca-certificates wget locales

RUN echo 'en_US.UTF-8 UTF-8' >/etc/locale.gen \
	&& locale-gen \
	&& update-locale LANG=en_US.UTF-8

ENV UWS_UID=3000
ENV UWS_GID=3000

RUN groupadd -g ${UWS_GID} uws \
	&& useradd -d /home/uws -m -c 'uws' -g ${UWS_GID} -u ${UWS_UID} uws \
	&& chmod -v 0750 /home/uws

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

ENTRYPOINT exec /usr/sbin/nologin
