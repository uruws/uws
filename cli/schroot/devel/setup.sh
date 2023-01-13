#!/bin/sh
set -eu

prof=uwscli

# debootstrap

debdist=$(cat ./cli/schroot/devel/${prof}/debian.distro)

if ! test -d /opt/uws/chroot/uwscli-devel; then
	PATH=/usr/sbin:${PATH}
	doas /usr/sbin/debootstrap --variant=minbase \
		"${debdist}" /opt/uws/chroot/uwscli-devel \
		http://deb.debian.org/debian/
fi

# schroot configure

doas rm -rf /etc/schroot/${prof}-devel
doas cp -va ./cli/schroot/devel/${prof} /etc/schroot/${prof}-devel
doas cp -va ./cli/schroot/devel/${prof}.conf /etc/schroot/chroot.d/${prof}-devel.conf
doas chown -v root:uws /etc/schroot/chroot.d/${prof}-devel.conf

# debian install

debpkg=$(cat ./cli/schroot/devel/${prof}/debian.install)

schroot_src="doas schroot -c source:${prof}-devel"

${schroot_src} -d /root -u root -- apt-get -q update -yy

echo ${debpkg} | xargs ${schroot_src} -d /root -u root -- \
	/srv/home/uwscli/sbin/apt-install.sh

echo 'permit nopass keepenv setenv { PATH } :uws as root' |
	${schroot_src} -d /root -u root -- tee /etc/doas.conf

echo 'es_US.UTF-8 UTF-8' |
	${schroot_src} -d /root -u root -- tee /etc/locale.gen

${schroot_src} -d /root -u root -- locale-gen

exit 0
