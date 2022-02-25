# Help

Once you are in the productions server, run `uwshelp` command to get a brief
description of all the available commands.

Run `uwshelp <cmd>` to get more information about an specific util.

# Jobs queue

Some commands, like in example `app-build`, add the job to the tasks queue so
the job can run in the background to avoid connection issues and to ensure that
no more than one (large/big) job will be running at the same time.

To check the queue status you can use `uwsq` util, which will show the current
status of the queue.

Check `uwshelp uwsq` to get more information about `uwsq` usage.

# Operations

## Build

To build a new release:

    app-build <app> X.Y.Z

Where *X.Y.Z* is a release tag in the <app> git repository.

Check `uwshelp app-build` for more information.

## Deploy

Deploy is only allowed for *admin* and *operator* users.

To check available releases for deploy run:

    app-deploy <app>

To deploy a release run:

    app-deploy <app> X.Y.Z

Where *X.Y.Z* is the built tag.

Check `uwshelp app-deploy` for more information.
