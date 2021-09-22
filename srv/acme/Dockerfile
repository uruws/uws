FROM uws/base-2109

LABEL maintainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="210922"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh python3 git python3-pip python3-setuptools python3-wheel \
	&& pip3 install --system 'git+https://github.com/diafygi/acme-tiny.git@master' \
	&& rm -vrf /root/.cache \
	&& /root/bin/apt-autoremove.sh git python3-pip python3-setuptools python3-wheel

RUN mkdir -vp -m 0755 /home/uws/bin
ADD --chown=root:root ./utils /home/uws/bin
RUN chmod -v 0755 /home/uws/bin/*.sh

VOLUME /srv/acme
ENV ACME_HOME /srv/acme

RUN mkdir -vp -m 0750 ${ACME_HOME} && chown -v uws:uws ${ACME_HOME}

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws
ENV PATH /home/uws/bin:${PATH}

CMD exec /bin/bash -l
