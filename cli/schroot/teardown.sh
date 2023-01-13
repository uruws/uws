#!/bin/sh
set -eux

profile=${1:?'profile?'}

surun='sudo -n'

${surun} rm -rf /srv/uwscli/${profile}

${surun} rm -rf /etc/schroot/uwscli-${profile}
${surun} rm -rf /etc/schroot/uwscli-${profile}-src

${surun} rm -rf /srv/uwscli/schroot

exit 0
