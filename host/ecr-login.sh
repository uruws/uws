#!/bin/sh
set -eu

AWS_REGION=${1:-'us-east-1'}

rm -vf /var/tmp/uws-docker-login.*
tmpfn=$(mktemp /var/tmp/uws-docker-login.XXXXXXXX)

aws ecr get-login --region ${AWS_REGION} | sed 's/-e none //' >${tmpfn}

chmod -v 0755 ${tmpfn}
/bin/sh ${tmpfn}
rm -vf ${tmpfn}

exit 0
