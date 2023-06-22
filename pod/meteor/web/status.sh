#!/bin/sh
echo 'webcdn'
~/pod/meteor/webcdn/status.sh
echo 'web'
exec ~/pod/meteor/status.sh web
