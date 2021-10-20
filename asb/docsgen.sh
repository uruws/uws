#!/bin/sh
set -eu
mkdir -vp ~/tmp/ansible-doc
cd ~/tmp/ansible-doc

echo '*** asbdoc.l'
ansible-doc -l >asbdoc.l

for m in $(grep -vE '^\w+\.' asbdoc.l | cut -d ' ' -f 1); do
	touch ${m}.txt
done

for m in $(grep -E '^community\.general\.docker\.' asbdoc.l | cut -d ' ' -f 1); do
	touch ${m}.txt
done

for m in $(grep -E '^community\.docker\.' asbdoc.l | cut -d ' ' -f 1); do
	touch ${m}.txt
done

for m in $(grep -E '^community\.kubernetes\.' asbdoc.l | cut -d ' ' -f 1); do
	touch ${m}.txt
done

for fn in $(ls *.txt); do
	asbdoc=$(basename ${fn} .txt)
	echo "*** ${fn}"
	if ! test -s ${fn}; then
		ansible-doc ${asbdoc} >${fn}
	fi
done

exit 0
