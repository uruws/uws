#!/bin/sh
set -eu
mkdir -vp ~/tmp/ansible-doc
cd ~/tmp/ansible-doc

echo '*** l.txt'
ansible-doc -l >l.txt

for m in $(grep -vE '^\w+\.' l.txt | cut -d ' ' -f 1); do
	touch ${m}.txt
done

for m in $(grep -E '^community\.docker\.' l.txt | cut -d ' ' -f 1 | cut -d '.' -f 3); do
	touch ${m}.txt
done

for fn in $(ls *.txt); do
	asbdoc=$(basename ${fn} .txt)
	echo "*** ${asbdoc}"
done

exit 0
