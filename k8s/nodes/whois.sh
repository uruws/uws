#!/bin/sh
set -eu
miss_address=${1:?'miss_address.txt?'}
cat ${miss_address} | while read addr; do
	echo -n "${addr}: "
	echo $(whois ${addr} | grep -E 'CDIR:|NetName:|Organization:|City:|Country:')
done
exit 0
