#!/bin/bash
set -u

echo 'WARNING: deleting mon namespace will destroy storage devices!!!'
echo
uwskube get pvc -n mon
echo

CONFIRM='N'
read -r -p 'are you sure? [N/y]: ' CONFIRM

if test 'Xy' = "X${CONFIRM}"; then
	echo "delete mon namespace and all its resources..."
	~/k8s/mon/rollin.sh
	exec uwskube delete namespace mon
else
	echo 'abort!'
	exit 1
fi
