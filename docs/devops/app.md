# App devel operations

Brief guide about build and deploy of the App.

Check [uwscli](./../devops.md) for usage information.

## Build

    $ app-build app X.Y.Z

X.Y.Z is the release tag you want to build.

Check the build progress with `uwsq`.

    $ uwsq

## Deploy

The App infra is split in 3 different clusters: app-east, app-west and worker.
app-east and app-west are the web containers running in two separate regions,
the workers run on its own separte cluster.

So the idea is to deploy them *one at a time* trying to reduce end user impact
in case of a failure.

### Workers cluster

Deploy:

    $ app-deploy worker X.Y.X-bpV

X.Y.Z-bpV is the release tag we built in previous step, with the buildpack version included (ie: 2.49.1-bp1).

Check deploy status:

    $ app-status worker

Check logs:

    $ app-logs worker -f

Once you are certain that it all worked as expected, deploy the web clusters.

### East web cluster

Deploy:

    $ app-deploy app-east X.Y.Z-bpV

Check deploy status:

    $ app-status app-east

Check logs:

    $ app-logs app-east -f

Once you are certain that it all worked as expected, deploy the other web cluster.

### West web cluster

Deploy:

    $ app-deploy app-west X.Y.Z-bpV

Check deploy status:

    $ app-status app-west

Check logs:

    $ app-logs app-west -f
