FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.4.16"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh awscli python3 less

RUN chgrp uws /usr/local/bin && chmod g+w /usr/local/bin

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN wget https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl \
	&& wget https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl.sha256 \
	&& sha256sum -c kubectl.sha256 \
	&& install -v -m 0755 kubectl /usr/local/bin \
	&& rm -vf kubectl kubectl.sha256

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

RUN printf 'export PATH="/home/uws/bin:${PATH}"\n' >>.bashrc

CMD exec /usr/local/bin/uws-login.sh
