# TalkingPoints Operations

Operations tasks using `uwscli` command line interface.

## SSH access

You need to access to the operations server using SSH:

    $ ssh -l uwscli ops.uws.talkingpts.org

Your ssh credentials need to be authorized first so contact your sysadmin if
that doesn't work for you.

## Help

Once you are in the productions server, run `uwshelp` command to get a brief
description of all the available commands.

Run `uwshelp <cmd>` to get more information about an specific util.

## Jobs queue

Some commands, like in example `meteor-build`, add the job to the tasks queue so
the job can be run in the background and to ensure that it will be only one job
running at the time.

To check the queue status you use `uwsq` util, which will show the current
status of the queue.

Check `uwshelp uwsq` to get more information about `uwsq` usage.
