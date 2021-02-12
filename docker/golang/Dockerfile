FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.12"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh golang-go

RUN mkdir -vp /go/src/uws \
	&& chown -vR uws:uws /go \
	&& chmod -vR 0750 /go
VOLUME /go/src/uws

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws
ENV GOPATH /go
ENV PATH /go/bin:${PATH}

WORKDIR /go/src/uws
ENTRYPOINT ["/usr/bin/go"]
