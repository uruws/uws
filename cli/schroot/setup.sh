#!/bin/sh
set -eu

profile=${1:?'profile?'}

CA_SMTPS='smtps/211006'

if ! test -s ./cli/schroot/${profile}/VERSION; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

version=$(cat ./cli/schroot/${profile}/VERSION)
echo "*** ${profile}/chroot.${version}"

surun='sudo -n'
schroot_src="${surun} schroot -c source:uwscli-${profile}-src"

#
# debootstrap
#

debdist=$(cat ./cli/schroot/debian.distro)

${surun} install -v -d -o root -g uws -m 0750 /srv/uwscli/${profile}
${surun} install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/union
${surun} install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/union/overlay
${surun} install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/union/underlay

debian_install='false'

cksum() (
	sha256sum ./cli/schroot/setup.sh ./cli/schroot/debian.distro ./cli/schroot/debian.install
)

LAST='NONE'
curfn=/srv/uwscli/${profile}/.check
if test -s "${curfn}"; then
	LAST=$(${surun} cat ${curfn})
fi

CUR=$(cksum)

if test "X${CUR}" = 'XNONE'; then
	debian_install='true'
fi
if test "X${CUR}" != "X${LAST}"; then
	debian_install='true'
fi

if ! test -d /srv/uwscli/${profile}/chroot.${version}; then
	debian_install='true'
	PATH=/usr/sbin:${PATH}
	${surun} /usr/sbin/debootstrap --variant=minbase \
		"${debdist}" /srv/uwscli/${profile}/chroot.${version} \
		http://deb.debian.org/debian/
fi

#
# OS setup
#

echo "uwscli-${profile}" | ${surun} tee /srv/uwscli/${profile}/chroot.${version}/etc/hostname

#
# schroot configure
#

${surun} rm -rf /etc/schroot/uwscli-${profile}
${surun} cp -va ./cli/schroot/${profile}/uwscli \
	/etc/schroot/uwscli-${profile}
${surun} cp -va ./cli/schroot/${profile}/uwscli.conf \
	/etc/schroot/chroot.d/uwscli-${profile}.conf
${surun} chown -v root:uws /etc/schroot/chroot.d/uwscli-${profile}.conf

${surun} rm -rf /etc/schroot/uwscli-${profile}-src
${surun} cp -va /etc/schroot/uwscli-${profile} \
	/etc/schroot/uwscli-${profile}-src
${surun} cp -va /etc/schroot/uwscli-${profile}/fstab.setup \
	/etc/schroot/uwscli-${profile}-src/fstab

#
# helper scripts
#

${surun} install -v -d -o root -g uws -m 0750 /srv/uwscli/schroot

${surun} install -v -C -o root -g uws -m 0750 ./cli/schroot/start.sh \
	/srv/uwscli/schroot/start.sh
${surun} install -v -C -o root -g uws -m 0750 ./cli/schroot/stop.sh \
	/srv/uwscli/schroot/stop.sh
${surun} install -v -C -o root -g uws -m 0750 ./cli/schroot/make.sh \
	/srv/uwscli/schroot/make.sh

#
# env setup
#

${surun} install -v -d -o 3000 -g 3100 -m 0750 /srv/uwscli/${profile}/run
${surun} install -v -d -o root -g root -m 0751 /srv/uwscli/${profile}/user
${surun} install -v -d -o root -g 3100 -m 0750 /srv/uwscli/${profile}/home
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/utils
${surun} install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/secret
${surun} install -v -d -o root -g root -m 0710 /srv/uwscli/${profile}/docker
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/build
${surun} install -v -d -o 3000 -g 3000 -m 0750 /srv/uwscli/${profile}/build/golang
${surun} install -v -d -o 3000 -g 3000 -m 0750 /srv/uwscli/${profile}/deploy
${surun} install -v -d -o 3000 -g 3000 -m 0750 /srv/uwscli/${profile}/logs
${surun} install -v -d -o 3000 -g 3000 -m 0750 /srv/uwscli/${profile}/syslog

#
# symlink latest chroot
#

if test -d /srv/uwscli/${profile}/chroot; then
	${surun} rm -rf /srv/uwscli/${profile}/chroot
fi

${surun} ln -svf /srv/uwscli/${profile}/chroot.${version}  /srv/uwscli/${profile}/chroot

#
# debian install
#

if test 'Xtrue' = "X${debian_install}"; then
	debpkg=$(cat ./cli/schroot/debian.install)

	${schroot_src} -d /root -u root -- apt-get -q update -yy

	echo ${debpkg} | xargs ${schroot_src} -d /root -u root -- \
		/srv/home/uwscli/sbin/apt-install.sh

	echo 'es_US.UTF-8 UTF-8' |
		${schroot_src} -d /root -u root -- tee /etc/locale.gen

	${schroot_src} -d /root -u root -- locale-gen
fi

cksum | ${surun} tee ${curfn}

#
# sync utils
#

${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/ca
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/ca/smtps
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/ca/smtps/client
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/utils/docker
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/utils/eks
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/utils/secret
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/utils/tmp
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/uws
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/uws/bin

rsync="${surun} rsync -xrltDp --delete-before"

echo '*** sync: home'
${rsync} --exclude=__pycache__ \
	./host/assets/jsbatch/srv/home/uwscli/ /srv/uwscli/${profile}/home/

echo '*** sync: secret'
${rsync} ./secret/cli/schroot/${profile}/ /srv/uwscli/${profile}/secret/

echo '*** sync: CA smtps'
${rsync} ./secret/ca/uws/${CA_SMTPS}/rootCA.pem \
	./secret/ca/uws/${CA_SMTPS}/rootCA-crl.pem \
	/srv/uwscli/${profile}/ca/smtps/
${rsync} ./secret/ca/uws/${CA_SMTPS}/client/08082dca-8d77-5c81-9a44-94642089b3b1.pem \
	./secret/ca/uws/${CA_SMTPS}/client/08082dca-8d77-5c81-9a44-94642089b3b1.key \
	/srv/uwscli/${profile}/ca/smtps/client/

echo '*** sync: Makefile'
${rsync} \
	./Makefile /srv/uwscli/${profile}/utils/Makefile

echo '*** sync: cli'
${rsync} --exclude=schroot --exclude='test*' \
	./cli/ /srv/uwscli/${profile}/utils/cli/

echo '*** sync: pod'
${rsync} --exclude=build \
	./pod/ /srv/uwscli/${profile}/utils/pod/

echo '*** sync: docker/base'
${rsync} --exclude=build --exclude=tmp \
	./docker/base/ /srv/uwscli/${profile}/utils/docker/base/

echo '*** sync: docker/golang'
${rsync} --exclude=build --exclude=tmp \
	./docker/golang/ /srv/uwscli/${profile}/utils/docker/golang/
${surun} install -v -d -o root -g root -m 0755 \
	/srv/uwscli/${profile}/utils/docker/golang/build
${surun} install -v -d -o root -g root -m 0755 \
	/srv/uwscli/${profile}/utils/docker/golang/tmp

echo '*** sync: docker/k8s'
${rsync} --exclude=build --exclude=tmp \
	./docker/k8s/ /srv/uwscli/${profile}/utils/docker/k8s/
${surun} install -v -d -o root -g root -m 0755 \
	/srv/uwscli/${profile}/utils/docker/k8s/build

echo '*** sync: k8s'
${rsync} --exclude=build --exclude=tmp --exclude=/test \
	./k8s/ /srv/uwscli/${profile}/utils/k8s/

echo '*** sync: eks'
${rsync} --exclude=build --exclude=tmp \
	./eks/env/ /srv/uwscli/${profile}/utils/eks/env/

echo '*** sync: secret/eks'
${rsync} \
	./secret/eks/ /srv/uwscli/${profile}/utils/secret/eks/

echo '*** sync: go'
${rsync} \
	./go/ /srv/uwscli/${profile}/utils/go/

# uws utils

${surun} install -v -C -o root -g 3000 -m 0750 \
	./host/assets/jsbatch/uws/bin/uwscli-logs.sh \
	/srv/uwscli/${profile}/uws/bin/uwscli-logs.sh

# host/cluster utils

${surun} install -v -d -o root -g 3100 -m 0750 /srv/uwscli/${profile}/utils/host
${surun} install -v -C -o root -g 3100 -m 0750 \
	./host/ecr-login.sh /srv/uwscli/${profile}/utils/host/ecr-login.sh

${surun} install -v -d -o root -g 3100 -m 0750 /srv/uwscli/${profile}/utils/cluster
${surun} install -v -C -o root -g 3100 -m 0750 \
	./cluster/ecr-push.sh /srv/uwscli/${profile}/utils/cluster/ecr-push.sh

#
# uwscli setup
#

${schroot_src} -d /root -u root -- install -v -d -o root -g 3100 -m 0750 \
	/etc/uws/cli
${schroot_src} -d /root -u root -- install -v -C -o root -g 3100 -m 0640 \
	/usr/local/etc/local_conf.py \
	/etc/uws/cli/local_conf.py

${schroot_src} -d /root -u root -- /srv/home/uwscli/sbin/uwscli_setup.py

exit 0
