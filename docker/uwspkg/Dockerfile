FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.02.16"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ENV UPKG_V 20210324
ENV UPKG_C 83e5eff257576b4d75702c626f5c5c23bd1d1f7ef1f0807b70ab33e907692ff6

RUN /root/bin/apt-install.sh libbsd0 libarchive13

RUN wget https://github.com/uruws/uwspkg/releases/download/v${UPKG_V}/uwspkg-bootstrap-${UPKG_V}.tgz \
	&& printf '%s  uwspkg-bootstrap-%s.tgz' ${UPKG_C} ${UPKG_V} >uwspkg-bootstrap.checksum \
	&& sha256sum -c uwspkg-bootstrap.checksum \
	&& tar -C / -vxf uwspkg-bootstrap-${UPKG_V}.tgz \
	&& rm -vf uwspkg-bootstrap-${UPKG_V}.tgz uwspkg-bootstrap.checksum \
	&& uwspkg info -a

ENTRYPOINT /usr/local/bin/uwspkg
