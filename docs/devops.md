# TalkingPoints Operations

Operations tasks using `uwscli` command line interface.

## SSH access

You need to access to the operations server using SSH:

    $ ssh -l <your_username> ops.uws.talkingpts.org

Your ssh credentials need to be authorized first so contact your sysadmin if
that doesn't work for you.

## Help

Once you are in the productions server, run `uwshelp` command to get a brief
description of all the available commands.

Run `uwshelp <cmd>` to get more information about an specific util.

## Jobs queue

Some commands, like in example `app-build`, add the job to the tasks queue so
the job can run in the background to avoid connection issues and to ensure that
no more than one (large/big) job will be running at the same time.

To check the queue status you can use `uwsq` util, which will show the current
status of the queue.

Check `uwshelp uwsq` to get more information about `uwsq` usage.

# Meteor Operations

## Build

To build a new release of the meteor run:

    app-build app X.Y.Z

Where *X.Y.Z* is a release tag in the App git repository.

Check `uwshelp app-build` for more information.

## Deploy

Deploy is only allowed for *admin* users.

To check available releases for deploy run:

    app-deploy app

To deploy a release run:

    app-deploy app X.Y.Z-bpV

Where *X.Y.Z* is the tag from the git repository and *bpV* is the buildpack
version that created the release.

Check `uwshelp app-deploy` for more information.
