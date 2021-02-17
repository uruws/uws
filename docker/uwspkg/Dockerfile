FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias.tincan@gmail.com>"
LABEL version="2021.02.16"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ENV UPKG_V 20210218
RUN /root/bin/apt-install.sh libbsd0 libarchive13

RUN wget https://github.com/uruws/uwspkg/releases/download/v${UPKG_V}/uwspkg-bootstrap-${UPKG_V}.tgz \
	&& tar -C / -vxf uwspkg-bootstrap-${UPKG_V}.tgz \
	&& rm -vf uwspkg-bootstrap-${UPKG_V}.tgz \
	&& uwspkg info -a

ENTRYPOINT /usr/local/bin/uwspkg
