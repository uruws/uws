#!/bin/sh
set -eu

rm -vf /var/tmp/uws-docker-login.*
tmpfn=$(mktemp /var/tmp/uws-docker-login.XXXXXXXX)

aws ecr get-login --region us-east-1 | sed 's/-e none //' >${tmpfn}

chmod -v 0755 ${tmpfn}
/bin/sh ${tmpfn}
rm -vf ${tmpfn}

exit 0
