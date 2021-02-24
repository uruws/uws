FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.12"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh golang-go

RUN mkdir -vp /go/src/uws /go/.cache /go/bin /uws \
	&& chown -vR uws:uws /go /uws \
	&& chmod -vR 0750 /go /uws

VOLUME /go/src/uws
VOLUME /go/.cache

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws
ENV GOPATH /go
ENV GOENV /go/src/uws/go.env
ENV GOCACHE /go/.cache

RUN printf 'export PATH="%s:${PATH}"\n' /go/bin >>/home/uws/.profile
RUN printf 'test -s %s && source %s\n' /go/src/uws/env/devel.env /go/src/uws/env/devel.env >>/home/uws/.profile

WORKDIR /go/src/uws
ENTRYPOINT ["/usr/bin/go"]
