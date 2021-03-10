FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="2021.03.10"

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

RUN /root/bin/apt-install.sh apt-transport-https gnupg

# https://github.com/heroku/cli/blob/master/install-ubuntu.sh
RUN echo 'deb https://cli-assets.heroku.com/apt ./' >/etc/apt/sources.list.d/heroku.list \
	&& wget -O heroku.key https://cli-assets.heroku.com/apt/release.key \
	&& apt-key add heroku.key \
	&& rm -vf heroku.key \
	&& /root/bin/apt-install.sh heroku

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

RUN heroku version
CMD exec /usr/local/bin/uws-login.sh
