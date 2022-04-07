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

install -v -C -o root -g root -m 0640
	/usr/local/etc/sshd/uwscli.conf \
	/etc/ssh/sshd_config.d/uwscli.conf

exec /usr/sbin/sshd -D -e -4 -q
