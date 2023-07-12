#!/bin/sh
set -eu

FQDN=${1:?'fqdn?'}
HOST=${2:?'host?'}

TMP=${PWD}/tmp/host/deploy/${HOST}
rm -rf ${TMP}
mkdir -vp ${TMP}

CLOUDD=${TMP}/cloud-init
mkdir -vp ${CLOUDD}

# gen config files

for fn in $(ls ./host/config/??_all_*.cfg ./host/config/??_${HOST}_*.cfg); do
	dst="${CLOUDD}/99zzzuws_$(basename ${fn})"
	cp -vf ${fn} ${dst}
done

# gen assets

init="${CLOUDD}/99zzzuws_deploy.sh"
cat ./host/cloud-init.sh >${init}

sush="${CLOUDD}/99zzzuws_setup.sh"
cat ./host/setup.sh >${sush}

# create assets archive

SHAR='shar --compactor=xz --no-timestamp --no-i18n --quiet'
ASSETS_SRC=${PWD}/host/assets/${HOST}
ASSETS=${TMP}/assets

# host assets
rsync -ax "${ASSETS_SRC}/" "${ASSETS}/"

TOOLS="${ASSETS}/srv/uws/deploy"
install -d "${TOOLS}"

# deploy tools: Makefile
rsync -ax "${PWD}/Makefile" "${TOOLS}/"

# deploy tools: docker
install -d "${TOOLS}/docker"
rsync -ax "${PWD}/docker/base/" "${TOOLS}/docker/base/"

# deploy tools: acme
install -d "${TOOLS}/srv/acme"
rsync -ax "${PWD}/srv/acme/" "${TOOLS}/srv/acme/"

# deploy tools: munin
##install -d "${TOOLS}/srv/munin"
##rsync -ax "${PWD}/srv/munin/" "${TOOLS}/srv/munin/"

# deploy tools: munin-backend
##install -d "${TOOLS}/srv/munin-backend"
##rsync -ax "${PWD}/srv/munin-backend/" "${TOOLS}/srv/munin-backend/"

# deploy tools: CA smtps
##install -d "${TOOLS}/secret/ca/uws/smtps/230503"
##rsync -ax "${PWD}/secret/ca/uws/smtps/230503/" "${TOOLS}/secret/ca/uws/smtps/211006/"

# deploy tools: secret munin
##install -d "${TOOLS}/secret/eks/files/munin"
##rsync -ax "${PWD}/secret/eks/files/munin/" "${TOOLS}/secret/eks/files/munin/"

# host tools
tools_sync=${PWD}/host/assets/${HOST}-sync.sh
if test -x "${tools_sync}"; then
	/bin/sh -eu "${tools_sync}" "${TOOLS}"
fi

afn="${CLOUDD}/99zzzuws_assets.sh"
if test -d ${ASSETS}; then
	oldwd=${PWD}
	cd  ${ASSETS}
	${SHAR} --archive-name "${HOST}-assets" . >${afn}
	cd ${oldwd}
else
	echo '#!/bin/sh' >${afn}
	echo 'exit 0' >>${afn}
fi

# clean host setup files and sync new ones

SSH="ssh -i ${PWD}/secret/aws.host/uws-host.pem -l admin"
chmod -v 0600 ${PWD}/secret/aws.host/uws-host.pem

if test "X${FQDN}" = 'Xlocal'; then
	echo "i - local deploy ${HOST}"

	sudo rm -vf /etc/cloud/cloud.cfg.d/99zzzuws_*.cfg
	sudo rsync -vrx ${CLOUDD}/*.* /etc/cloud/cloud.cfg.d/

	sudo chmod -v 0755 /etc/cloud/cloud.cfg.d/99zzzuws_deploy.sh
	sudo /etc/cloud/cloud.cfg.d/99zzzuws_deploy.sh
else
	${SSH} ${FQDN} 'sudo chgrp -v admin /etc/cloud/cloud.cfg.d && sudo chmod -v g+w /etc/cloud/cloud.cfg.d && sudo rm -vf /etc/cloud/cloud.cfg.d/99zzzuws_*.cfg'

	rsync -vrx -e "${SSH}" ${CLOUDD}/*.* ${FQDN}:/etc/cloud/cloud.cfg.d/

	${SSH} ${FQDN} 'sudo chmod -v 0755 /etc/cloud/cloud.cfg.d/99zzzuws_deploy.sh && nq -c sudo /etc/cloud/cloud.cfg.d/99zzzuws_deploy.sh'
fi

#rm -rf ${TMP}
exit 0
