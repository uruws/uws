#!/bin/sh
set -eu

install -v -d -o root -g root -m 0755 /run/sshd

install -v -C -o root -g root -m 0600 \
	/usr/local/etc/sshd/ssh_host_rsa_key \
	/etc/ssh/ssh_host_rsa_key
install -v -C -o root -g root -m 0640 \
	/usr/local/etc/sshd/ssh_host_rsa_key.pub \
	/etc/ssh/ssh_host_rsa_key.pub

install -v -C -o root -g root -m 0600 \
	/usr/local/etc/sshd/ssh_host_ecdsa_key \
	/etc/ssh/ssh_host_ecdsa_key
install -v -C -o root -g root -m 0640 \
	/usr/local/etc/sshd/ssh_host_ecdsa_key.pub \
	/etc/ssh/ssh_host_ecdsa_key.pub

install -v -C -o root -g root -m 0600 \
	/usr/local/etc/sshd/ssh_host_ed25519_key \
	/etc/ssh/ssh_host_ed25519_key
install -v -C -o root -g root -m 0640 \
	/usr/local/etc/sshd/ssh_host_ed25519_key.pub \
	/etc/ssh/ssh_host_ed25519_key.pub

install -v -C -o root -g root -m 0640 \
	/usr/local/etc/sshd/uwscli.conf \
	/etc/ssh/sshd_config.d/uwscli.conf

# monit workaround
touch /etc/ssh/ssh_host_dsa_key
chown -v root:root /etc/ssh/ssh_host_dsa_key
chmod -v 0600      /etc/ssh/ssh_host_dsa_key

# monit
ln -svf /etc/monit/conf-available/openssh-server /etc/monit/conf-enabled

/etc/init.d/ssh start
exit 0
