#!/bin/sh
set -eu

FQDN=${1:?'fqdn?'}
HOST=${2:?'host?'}

TMP=${PWD}/tmp/host/deploy/${HOST}
rm -rf ${TMP}
mkdir -p ${TMP}

for fn in $(ls ./host/config/??_all_*.cfg ./host/config/??_${HOST}_*.cfg); do
	dst="${TMP}/99zzzuws_$(basename ${fn})"
	cp -vf ${fn} ${dst}
done

ssh -i ~/.ssh/uws-host.pem -l admin ${FQDN} 'sudo chgrp -v admin /etc/cloud/cloud.cfg.d && sudo chmod -v g+w /etc/cloud/cloud.cfg.d && sudo rm -vf /etc/cloud/cloud.cfg.d/99zzzuws_*.cfg'

rsync -vax -e 'ssh -i ~/.ssh/uws-host.pem -l admin' ${TMP}/*.cfg \
	${FQDN}:/etc/cloud/cloud.cfg.d/

sleep 1
echo "reboot..."
ssh -i ~/.ssh/uws-host.pem -l admin ${FQDN} 'sudo reboot'

exit 0
