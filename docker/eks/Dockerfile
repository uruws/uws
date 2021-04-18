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

# https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
RUN wget -O helm.tgz https://get.helm.sh/helm-v3.5.4-linux-amd64.tar.gz \
	&& tar -vxzf helm.tgz \
	&& install -v -m 0755 linux-amd64/helm /usr/local/bin \
	&& rm -rvf helm.tgz linux-amd64

RUN install -v -d -m 0750 /home/uws/.kube/eksctl/clusters \
	&& install -v -d -m 0750 /home/uws/.aws \
	&& install -v -d -m 0750 /home/uws/bin \
	&& install -v -d -m 0750 /home/uws/files

VOLUME /home/uws/.kube/eksctl/clusters
VOLUME /home/uws/.aws
VOLUME /home/uws/bin
VOLUME /home/uws/files

RUN printf 'export PATH="/home/uws/bin:${PATH}"\n' >>.bashrc

CMD exec /usr/local/bin/uws-login.sh
