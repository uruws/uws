FROM amazon/aws-cli

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.02"

ARG UWS_UID=1000
ARG UWS_GID=1000

RUN echo "uws:x:${UWS_GID}:" >>/etc/group
RUN echo "uws:x:${UWS_UID}:${UWS_GID}:uws:/home/uws:/bin/bash" >>/etc/passwd
RUN echo >>/etc/shadow; echo 'uws:*LOCK*:14600::::::' >>/etc/shadow

RUN mkdir -vp /home/uws \
	&& chown -v uws:uws /aws /home/uws \
	&& chmod -v 0750 /aws /home/uws

USER uws:uws
WORKDIR /aws

ENV USER uws
ENV HOME /home/uws

ARG UWS_UMASK=0027
RUN printf 'umask %s\n' ${UWS_UMASK} >>/home/uws/.profile
