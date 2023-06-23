FROM debian:bookworm-20230502-slim

ARG UWS_VERSION

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="${UWS_VERSION}"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ADD ./utils/apt-*.sh /root/bin/
RUN chmod -v 0750 /root/bin /root/bin/*.sh

RUN /root/bin/apt-distupgrade.sh
RUN /root/bin/apt-install.sh bash ca-certificates wget locales

ADD ./utils/uws-*.sh /root/bin/
RUN chmod -v 0750 /root/bin /root/bin/*.sh \
	&& install -m 0755 /root/bin/uws-login.sh /usr/local/bin/uws-login.sh

RUN echo 'en_US.UTF-8 UTF-8' >/etc/locale.gen \
	&& locale-gen \
	&& update-locale LANG=en_US.UTF-8

ARG UWS_UID=1000
ARG UWS_GID=1000

ENV UWS_UID ${UWS_UID}
ENV UWS_GID ${UWS_GID}

RUN groupadd -o -g ${UWS_GID} uws \
	&& useradd -o -d /home/uws -m -c 'uws' -g ${UWS_GID} -u ${UWS_UID} uws \
	&& chmod -v 0750 /home/uws

RUN groupadd -o -g 1500 uwsops \
	&& useradd -o -d /home/uwsops -m -c 'uwsops' -g 1500 -u 1500 uwsops \
	&& chmod -v 0750 /home/uwsops

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

ARG UWS_UMASK=0027

RUN printf 'umask %s\n' ${UWS_UMASK} >>/home/uws/.profile
RUN printf "export PS1='%s '\n" '\u@\h:\W\$' >>/home/uws/.profile

CMD exec /bin/bash -l
