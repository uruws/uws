FROM debian:buster-slim

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.01"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get clean \
	&& apt-get update \
	&& apt-get dist-upgrade -yy --purge \
	&& apt-get install -yy --no-install-recommends dash \
	&& apt-get clean \
	&& apt-get autoremove -yy --purge \
	&& rm -rf /var/lib/apt/lists/* \
		/var/cache/apt/archives/*.deb \
		/var/cache/apt/*cache.bin

ARG UWS_UID=1000
ARG UWS_GID=1000

RUN groupadd -g ${UWS_GID} uws \
	&& useradd -d /home/uws -m -c 'uws' -g ${UWS_GID} -u ${UWS_UID} uws \
	&& chmod -v 0750 /home/uws \
	&& mkdir -vp /uws \
	&& chmod -v 0750 /uws \
	&& chown -v uws:uws /uws

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

ARG UWS_UMASK=0027

RUN printf 'umask %s\n' ${UWS_UMASK} >>/home/uws/.profile
RUN printf "export PS1='%s '\n" '\h:\W\$' >>/home/uws/.profile
RUN printf "export PATH=/uws/bin:/usr/local/bin:/usr/bin:/bin\n" >>/home/uws/.profile

CMD exec /bin/sh -l
