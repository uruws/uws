FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="20210624"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh gettext-base awscli python3

RUN chgrp ${UWS_GID} /usr/local/bin && chmod g+w /usr/local/bin

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

ENV KUBE_VERSION 1.19.6/2021-01-05
ENV KUBE_URL https://amazon-eks.s3.us-west-2.amazonaws.com/${KUBE_VERSION}

RUN wget ${KUBE_URL}/bin/linux/amd64/kubectl \
	&& wget ${KUBE_URL}/bin/linux/amd64/kubectl.sha256 \
	&& sha256sum -c kubectl.sha256 \
	&& install -v -m 0755 kubectl /usr/local/bin \
	&& rm -vf kubectl kubectl.sha256

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

COPY ./utils/uwskube /tmp/uwskube
RUN install -v -m 0755 /tmp/uwskube /usr/local/bin/uwskube \
	&& rm -vf /tmp/uwskube

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws
