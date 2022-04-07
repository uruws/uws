#!/bin/sh
set -eu

profile=${1:?'profile?'}

if ! test -s ./cli/schroot/${profile}/VERSION; then
	echo "invalid profile: ${profile}" >&2
	exit 1
fi

version=$(cat ./cli/schroot/${profile}/VERSION)
echo "*** ${profile}/chroot.${version}"

surun='sudo'

# debootstrap

debdist=$(cat ./cli/schroot/${profile}/uwscli/debian.distro)

${surun} install -v -d -o root -g uws -m 0750 /srv/uwscli/${profile}
${surun} install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/union
${surun} install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/union/overlay
${surun} install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/union/underlay

if ! test -d /srv/uwscli/${profile}/chroot.${version}; then
	PATH=/usr/sbin:${PATH}
	${surun} /usr/sbin/debootstrap --variant=minbase \
		"${debdist}" /srv/uwscli/${profile}/chroot.${version} \
		http://deb.debian.org/debian/
fi

# schroot configure

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

# env setup

${surun} install -v -d -o root -g root -m 0751 /srv/uwscli/${profile}/user
${surun} install -v -d -o root -g 3100 -m 0750 /srv/uwscli/${profile}/home
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/utils
${surun} install -v -d -o root -g 3000 -m 0750 /srv/uwscli/${profile}/utils/tmp
${surun} install -v -d -o root -g root -m 0750 /srv/uwscli/${profile}/secret

# symlink latest chroot

if test -d /srv/uwscli/${profile}/chroot; then
	${surun} rm -rf /srv/uwscli/${profile}/chroot
fi

${surun} ln -svf /srv/uwscli/${profile}/chroot.${version}  /srv/uwscli/${profile}/chroot

# debian install

debpkg=$(cat ./cli/schroot/${profile}/uwscli/debian.install)

schroot_src="${surun} schroot -c source:uwscli-${profile}-src"

${schroot_src} -d /root -u root -- apt-get -q update -yy

echo ${debpkg} | xargs ${schroot_src} -d /root -u root -- \
	apt-get -q install -yy --purge --no-install-recommends

echo 'es_US.UTF-8 UTF-8' |
	${schroot_src} -d /root -u root -- tee /etc/locale.gen

${schroot_src} -d /root -u root -- locale-gen

# sync utils

# uwscli home
${surun} rsync -vxrltDp --delete-before --delete-excluded \
	--exclude=__pycache__ \
	./host/assets/jsbatch/srv/home/uwscli/ /srv/uwscli/${profile}/home/

# repo utils
${surun} rsync -vxrltDp --delete-before --delete-excluded \
	--exclude=schroot \
	--exclude='test*' \
	./cli/ /srv/uwscli/${profile}/utils/cli/

# secrets
${surun} rsync -vxrltDp --delete-before --delete-excluded \
	./secret/cli/schroot/${profile}/ /srv/uwscli/${profile}/secret/

# uwscli setup

${schroot_src} -d /root -u root -- install -v -d -o root -g uwscli -m 0750 \
	/etc/uws/cli
${schroot_src} -d /root -u root -- install -v -C -o root -g uwscli -m 0640 \
	/usr/local/etc/local_conf.py \
	/etc/uws/cli/local_conf.py

${schroot_src} -d /root -u root -- /srv/home/uwscli/sbin/uwscli_setup.py

${schroot_src} -d /root -u root -- rm -vf /var/run

exit 0
