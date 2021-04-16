FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.4.16"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh awscli kubernetes-client

RUN chgrp uws /usr/local/bin && chmod g+w /usr/local/bin

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN wget https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz \
	&& wget https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_checksums.txt \
	&& sha256sum --ignore-missing -c eksctl_checksums.txt \
	&& tar -C /tmp -xvzf eksctl_Linux_amd64.tar.gz \
	&& install -v -m 0755 /tmp/eksctl /usr/local/bin \
	&& rm -vf eksctl_*.* /tmp/eksctl

#USER root:root
#WORKDIR /root

#ENV USER root
#ENV HOME /root

#COPY --chown=uws:uws ./utils/*.sh /usr/local/bin/
#RUN chmod -v 0550 /usr/local/bin/*.sh

VOLUME /home/uws/.aws

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

CMD exec /usr/local/bin/uws-login.sh
