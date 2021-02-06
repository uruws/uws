#!/bin/sh
set -eu

FQDN=${1:?'fqdn?'}
HOST=${2:?'host?'}

TMP=${PWD}/tmp/host/deploy/${HOST}
rm -rf ${TMP}
mkdir -p ${TMP}

# gen config files

for fn in $(ls ./host/config/??_all_*.cfg ./host/config/??_${HOST}_*.cfg); do
	dst="${TMP}/99zzzuws_$(basename ${fn})"
	cp -vf ${fn} ${dst}
done

# gen assets

init="${TMP}/99zzzuws_deploy.sh"
cat ./host/cloud-init.sh >${init}

sush="${TMP}/99zzzuws_setup.sh"
cat ./host/setup.sh >${sush}

# create assets archive

SHAR='shar --compactor=xz --no-timestamp --no-i18n --quiet'
ASSETS=${PWD}/host/assets/${HOST}

afn="${TMP}/99zzzuws_assets.sh"
if test -d ${ASSETS}; then
	oldwd=${PWD}
	cd  ${ASSETS}
	${SHAR} --archive-name "${HOST}-assets" . >${afn}
	cd ${oldwd}
else
	echo '#!/bin/sh' >${afn}
	echo 'exit 0' >>${afn}
fi

# clean host setup files

SSH='ssh -i ~/.ssh/uws-host.pem -l admin'

${SSH} ${FQDN} 'sudo chgrp -v admin /etc/cloud/cloud.cfg.d && sudo chmod -v g+w /etc/cloud/cloud.cfg.d && sudo rm -vf /etc/cloud/cloud.cfg.d/99zzzuws_*.cfg'

# sync new setup files

rsync -vax -e "${SSH}" ${TMP}/*.* \
	${FQDN}:/etc/cloud/cloud.cfg.d/

${SSH} ${FQDN} 'sudo chmod -v 0755 /etc/cloud/cloud.cfg.d/99zzzuws_deploy.sh && nq -c sudo /etc/cloud/cloud.cfg.d/99zzzuws_deploy.sh'

exit 0
