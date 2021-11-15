#!/bin/sh
set -eu

refname="$1"
oldrev="$2"
newrev="$3"

if [ -z "$refname" -o -z "$oldrev" -o -z "$newrev" ]; then
	echo "usage: $0 <ref> <oldrev> <newrev>" >&2
	exit 1
fi

# --- Check types
# if $newrev is 0000...0000, it's a commit to delete a ref.
zero=$(git hash-object --stdin </dev/null | tr '[0-9a-f]' '0')
if [ "$newrev" = "$zero" ]; then
	newrev_type=delete
else
	newrev_type=$(git cat-file -t $newrev)
fi

case "$refname","$newrev_type" in
	refs/tags/*,commit)
		# un-annotated tag
		short_refname=${refname##refs/tags/}
		echo "*** The un-annotated tag, $short_refname, is not allowed in this repository" >&2
		echo "*** Use 'git tag [ -a | -s ]' for tags you want to propagate." >&2
		exit 1
	;;
	refs/tags/*,delete)
		# delete tag
		echo "*** Deleting a tag is not allowed in this repository" >&2
		exit 1
	;;
	refs/tags/*,tag)
		# annotated tag
		if git rev-parse $refname > /dev/null 2>&1
		then
			echo "*** Tag '$refname' already exists." >&2
			echo "*** Modifying a tag is not allowed in this repository." >&2
			exit 1
		fi
		export NQDIR=${HOME}/nq
		mkdir -p -m 0750 ${NQDIR}
		nq -c -- /srv/uws/deploy/cli/git-update-run.sh ${PWD} ${refname}
	;;
esac

exit 0
