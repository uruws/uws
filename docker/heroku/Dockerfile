FROM uws/base-testing

LABEL mantainer="Jeremías Casteglione <jeremias@talkingpts.org>"
LABEL version="221117"

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

RUN mkdir -vp ~/.cache/heroku
RUN heroku version \
	&& heroku plugins:install heroku-slugs

USER root:root
WORKDIR /root

ENV USER root
ENV HOME /root

COPY --chown=uws:uws ./utils/*.sh /usr/local/bin/
RUN chmod -v 0555 /usr/local/bin/*.sh

USER uws:uws
WORKDIR /home/uws

ENV USER uws
ENV HOME /home/uws

CMD exec /usr/local/bin/uws-login.sh
