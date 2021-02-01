FROM alpine:3

LABEL maintainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.01"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN apk upgrade --no-cache -U

ARG UWS_UID
ARG UWS_GID

RUN addgroup -g ${UWS_GID} uws \
	&& adduser -h /home/uws -g uws -s /bin/sh -G uws -D -u ${UWS_UID} uws

CMD exec /bin/sh -l
