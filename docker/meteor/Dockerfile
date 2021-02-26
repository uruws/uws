FROM uws/base

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.02.01"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

ADD ./meteor-bootstrap.sh /root/bin
RUN chmod -v 0750 /root/bin /root/bin/*.sh

#RUN /root/bin/meteor-bootstrap.sh

#USER uws:uws
#WORKDIR /home/uws

#ENV USER uws
#ENV HOME /home/uws

CMD exec /bin/bash -l
