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

SHAR='shar --compactor=xz --no-timestamp --no-i18n --quiet'
ASSETS=${PWD}/host/assets/${HOST}

selfextract() {
	echo '#!/bin/sh
# uws cloud-init selfextract host assets
if test "X${1}" = "X--selfextract"; then
	cd /
	shift
else
	exec ${0} --selfextract -c
fi'
}

if test -d ${ASSETS}; then
	dst="${TMP}/99zzzuws_70_${HOST}_assets.cfg"
	selfextract >${dst}
	oldwd=${PWD}
	cd  ${ASSETS}
	${SHAR} --archive-name "${HOST}-assets" . >>${dst}
	cd ${oldwd}
fi

SSH='ssh -i ~/.ssh/uws-host.pem -l admin'

${SSH} ${FQDN} 'sudo chgrp -v admin /etc/cloud/cloud.cfg.d && sudo chmod -v g+w /etc/cloud/cloud.cfg.d && sudo rm -vf /etc/cloud/cloud.cfg.d/99zzzuws_*.cfg'

rsync -vax -e "${SSH}" ${TMP}/*.cfg \
	${FQDN}:/etc/cloud/cloud.cfg.d/

sleep 1
read -p 'reboot? [yes/no]: ' yesno
if test "X${yesno}" = 'Xyes'; then
	echo "reboot..."
	${SSH} ${FQDN} 'sudo cloud-init clean && sudo rm -vf /var/log/cloud-init*.log && sudo reboot'
else
	echo "cloud-init clean..."
	${SSH} ${FQDN} 'sudo cloud-init clean'
fi

exit 0
