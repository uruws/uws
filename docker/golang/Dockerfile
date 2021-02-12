FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.12"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

#~ ADD ./utils /root/bin
#~ RUN chmod -v 0750 /root/bin /root/bin/*.sh

RUN /root/bin/apt-install.sh golang-go

RUN mkdir -vp /uws/src \
	&& chown -vR uws:uws /uws \
	&& chmod -vR 0750 /uws

USER uws:uws
ENV USER uws
ENV HOME /home/uws

WORKDIR /uws/src
ENTRYPOINT ["/usr/bin/go"]
