#!/bin/sh
set -eu

# debootstrap

debdist=$(cat ./cli/schroot/test/uwscli/debian.distro)

if ! test -d /opt/uws/chroot/uwscli-test; then
	PATH=/usr/sbin:${PATH}
	doas /usr/sbin/debootstrap --variant=minbase \
		"${debdist}" /opt/uws/chroot/uwscli-test \
		http://deb.debian.org/debian/
fi

# schroot configure

doas rm -rf /etc/schroot/uwscli-test
doas cp -va ./cli/schroot/test/uwscli /etc/schroot/uwscli-test
doas cp -va ./cli/schroot/test/uwscli.conf /etc/schroot/chroot.d/uwscli-test.conf
doas chown -v root:uws /etc/schroot/chroot.d/uwscli-test.conf

# env setup

doas install -v -d -o root -g root -m 0755 /srv/uwscli/test/user
doas install -v -d -o root -g root -m 0755 /srv/uwscli/test/home
doas install -v -d -o root -g root -m 0755 /srv/uwscli/test/utils

doas rsync -vxrltD --delete-before \
	./host/assets/jsbatch/srv/home/uwscli/ /srv/uwscli/test/home/

doas rsync -vxrltD --delete-before --exclude=./schroot --exclude='./test*' \
	./cli/ /srv/uwscli/test/utils/

# debian install

debpkg=$(cat ./cli/schroot/test/uwscli/debian.install)

schroot_src="doas schroot -c source:uwscli-test"

${schroot_src} -d /root -u root -- apt-get -q update -yy

echo ${debpkg} | xargs ${schroot_src} -d /root -u root -- \
	apt-get -q install -yy --purge --no-install-recommends

echo 'permit nopass keepenv setenv { PATH } :uws as root' |
	${schroot_src} -d /root -u root -- tee /etc/doas.conf

echo 'es_US.UTF-8 UTF-8' |
	${schroot_src} -d /root -u root -- tee /etc/locale.gen

${schroot_src} -d /root -u root -- locale-gen

exit 0
