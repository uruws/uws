#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -d ./cli/schroot/${profile}; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

# debootstrap

debdist=$(cat ./cli/schroot/${profile}/uwscli/debian.distro)

doas install -v -d -o root -g uws -m 0750 /srv/uwscli/${profile}
doas install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/union
doas install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/union/overlay
doas install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/union/underlay

if ! test -d /srv/uwscli/${profile}/chroot; then
	PATH=/usr/sbin:${PATH}
	doas /usr/sbin/debootstrap --variant=minbase \
		"${debdist}" /srv/uwscli/${profile}/chroot \
		http://deb.debian.org/debian/
fi

# schroot configure

doas rm -rf /etc/schroot/uwscli-${profile}
doas cp -va ./cli/schroot/${profile}/uwscli /etc/schroot/uwscli-${profile}
doas cp -va ./cli/schroot/${profile}/uwscli.conf /etc/schroot/chroot.d/uwscli-${profile}.conf
doas chown -v root:uws /etc/schroot/chroot.d/uwscli-${profile}.conf

# env setup

doas install -v -d -o root -g root -m 0751 /srv/uwscli/${profile}/user
doas install -v -d -o root -g 3100 -m 0750 /srv/uwscli/${profile}/home
doas install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/utils

doas rsync -vxrltDp --delete-before --delete-excluded \
	--exclude=__pycache__ \
	./host/assets/jsbatch/srv/home/uwscli/ /srv/uwscli/${profile}/home/

doas rsync -vxrltDp --delete-before --delete-excluded \
	--exclude=schroot \
	--exclude='test*' \
	./cli/ /srv/uwscli/${profile}/utils/cli/

# debian install

debpkg=$(cat ./cli/schroot/${profile}/uwscli/debian.install)

schroot_src="doas schroot -c source:uwscli-${profile}"

${schroot_src} -d /root -u root -- apt-get -q update -yy

echo ${debpkg} | xargs ${schroot_src} -d /root -u root -- \
	apt-get -q install -yy --purge --no-install-recommends

echo 'permit nopass keepenv setenv { PATH } :uws as root' |
	${schroot_src} -d /root -u root -- tee /etc/doas.conf

echo 'es_US.UTF-8 UTF-8' |
	${schroot_src} -d /root -u root -- tee /etc/locale.gen

${schroot_src} -d /root -u root -- locale-gen

exec ${schroot_src} -d /root -u root -- /srv/home/uwscli/sbin/uwscli_setup.py
