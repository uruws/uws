FROM uws/k8s-${K8S_TAG}-${DOCKER_TAG}

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="${DOCKER_VERSION}"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

# vim is needed for uwskube edit
RUN /root/bin/apt-install.sh less git vim-tiny

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN wget -q ${EKSCTL_URL}/eksctl_Linux_amd64.tar.gz \
	&& wget -q ${EKSCTL_URL}/eksctl_checksums.txt \
	&& sha256sum --ignore-missing -c eksctl_checksums.txt \
	&& tar -C /tmp -xvzf eksctl_Linux_amd64.tar.gz \
	&& install -v -m 0755 /tmp/eksctl /usr/local/bin \
	&& rm -vf eksctl_*.* /tmp/eksctl

RUN install -v -d -m 0750 /home/uws/.kube/eksctl/clusters \
	&& install -v -d -m 0750 /home/uws/.kube/cache \
	&& install -v -d -m 0750 /home/uws/.aws \
	&& install -v -d -m 0750 /home/uws/bin \
	&& install -v -d -m 0750 /home/uws/k8s \
	&& install -v -d -m 0750 /home/uws/pod \
	&& install -v -d -m 0750 /home/uws/cluster \
	&& install -v -d -m 0750 /home/uws/secret \
	&& install -v -d -m 0750 /home/uws/tmp

ENV AWS_PROFILE uwsdev
ENV AWS_REGION us-west-2
ENV UWS_CLUSTER uwsdev
