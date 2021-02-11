#!/bin/sh
set -eu

SERVICE=${1:?'service name?'}
shift
CHECK="/etc/systemd/system/${SERVICE}.service $@"

if test "X${CHECK}" = 'X'; then
	echo "ERROR - service restart ${SERVICE} no files to check" >&2
	exit 1
fi

BASEDIR=/srv/run/uws-service-restart
mkdir -vp ${BASEDIR}

lastfn=${BASEDIR}/${SERVICE}.last
if ! test -s ${lastfn}; then
	echo 'NONE' >${lastfn}
fi
LAST="$(cat ${lastfn})"

dockerimg=$(echo ${SERVICE} | sed '#uws-#uws/#')
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
	find ${CHECK} -type f 2>/dev/null >${checkfn}
	cat ${checkfn} | xargs sha256sum >${newfn}
	cat ${newfn} | sha256sum - | cut -d ' ' -f 1
}

CUR="$(cksum)"

if test "X${CUR}" != "X${LAST}"; then
	echo "i - restart service: ${SERVICE}"
	echo "i - diff:"
	diff -Naur ${curfn} ${newfn}
	echo "i - end diff"
	service ${SERVICE} restart
	cat ${newfn} >${curfn}
	echo "${CUR}" >${lastfn}
fi

exit 0
