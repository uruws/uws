#!/bin/sh
set -eu
AWS_REGION=${1:?'aws region?'}

rm -f /var/tmp/uws-docker-login.*
tmpfn=$(mktemp /var/tmp/uws-docker-login.XXXXXXXX)

aws ecr get-login --region ${AWS_REGION} | sed 's/-e none //' >${tmpfn}

/bin/sh ${tmpfn}

rm -vf ${tmpfn}
exit 0
