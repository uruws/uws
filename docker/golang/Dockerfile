FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.12"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh golang-go

RUN mkdir -vp /uws/src \
	&& chown -vR uws:uws /uws \
	&& chmod -vR 0750 /uws

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

WORKDIR /uws/src
ENTRYPOINT ["/usr/bin/go"]
