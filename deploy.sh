#!/bin/sh
set -eu
servername='ops.uws.talkingpts.org'
if ! git remote | grep -q deploy; then
	git remote add deploy "uws@${servername}:/srv/uws/deploy.git"
fi
deploy_run='TRUE'
check_run='TRUE'
tail_run='TRUE'
for arg in "$@"; do
	case ${arg} in
		--no-test|-T)
			check_run='FALSE'
		;;
		--no-logs|-L)
			tail_run='FALSE'
		;;
		--no-deploy|-D)
			deploy_run='FALSE'
		;;
		--debug)
			set -x
		;;
	esac
done
if test "X${check_run}" = 'XTRUE'; then
	check_cmd=""
	if which nice >/dev/null; then
		check_cmd="nice"
	fi
	if which ionice >/dev/null; then
		check_cmd="${check_cmd} ionice"
	fi
	check_cmd="${check_cmd} make check"
	${check_cmd}
fi
if test "X${deploy_run}" = 'XTRUE'; then
	git push
	git push deploy
	ssh_cmd="ssh -a -C -n -x"
	if which timeout >/dev/null; then
		ssh_cmd="timeout -k1830 1800 ${ssh_cmd}"
	fi
	if test "X${tail_run}" = 'XTRUE'; then
		exec ${ssh_cmd} -l uws "${servername}" tail -f /var/tmp/uws-deploy.log
	fi
fi
exit 0
