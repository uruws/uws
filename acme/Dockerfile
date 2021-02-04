FROM uws/base

LABEL maintainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.04"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh python3 git python3-pip python3-setuptools python3-wheel \
	&& pip3 install --system 'git+https://github.com/diafygi/acme-tiny.git@master' \
	&& rm -vrf /root/.cache \
	&& /root/bin/apt-autoremove.sh git python3-pip python3-setuptools python3-wheel

ENTRYPOINT exec /usr/local/bin/acme-tiny
