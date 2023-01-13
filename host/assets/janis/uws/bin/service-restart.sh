#!/bin/sh
set -eu

SERVICE=${1:?'service name?'}

shift
CHECK="/uws/bin/service-restart.sh /etc/systemd/system/${SERVICE}.service $*"

BASEDIR=/srv/run/uws-service-restart
mkdir -vp ${BASEDIR}

lastfn=${BASEDIR}/${SERVICE}.last
if ! test -s ${lastfn}; then
	echo 'NONE' >${lastfn}
fi
LAST="$(cat ${lastfn})"

dockerimg=${DOCKER_IMAGE:-'NOSET'}
if test "X${dockerimg}" = 'XNOSET'; then
	dockerimg=$(echo ${SERVICE} | sed 's#uws-#uws/#')
fi
dockerfn=${BASEDIR}/${SERVICE}.docker-image
(docker image inspect -f '{{.Id}}' ${dockerimg} >${dockerfn} 2>&1) || true

CHECK="${dockerfn} ${CHECK}"

curfn=${BASEDIR}/${SERVICE}.cur
if ! test -s ${curfn}; then
	echo 'EMPTY' >${curfn}
fi

newfn=${BASEDIR}/${SERVICE}.new
checkfn=${BASEDIR}/${SERVICE}.check
cksum() {
	find ${CHECK} -type f 2>/dev/null >${checkfn} || true
	cat ${checkfn} | xargs sha256sum >${newfn}
	cat ${newfn} | sha256sum - | cut -d ' ' -f 1
}

CUR="$(cksum)"

if test "X${CUR}" != "X${LAST}"; then
	echo "i - restart service: ${SERVICE}"
	echo "i - diff:"
	diff -Naur ${curfn} ${newfn} || true
	echo "i - end diff"
	systemctl restart ${SERVICE}.service
	cat ${newfn} >${curfn}
	echo "${CUR}" >${lastfn}
else
	if test 'Xfailed' = "X$(systemctl is-active ${SERVICE}.service || true)"; then
		echo "i - restart failed service: ${SERVICE}"
		systemctl reset-failed ${SERVICE}.service
		systemctl restart ${SERVICE}.service
	fi
fi

exit 0
