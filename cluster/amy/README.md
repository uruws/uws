# Amy

App web service.

We have 2 clusters running in 2 different AWS regions for the web service.
And another cluster for the workers.

* [Pod](../../pod/meteor/web/deploy.yaml)

## East

* [Env](../../eks/env/amy-east.env)

## West

* [Env](../../eks/env/amy-west.env)

## Worker

* [Env](../../eks/env/amy-wrkr.env)
* [Pod](../../pod/meteor/worker/deploy.yaml)

## Test

* [Test-1](../../eks/env/amy-test-1.env)
* [Test-2](../../eks/env/amy-test-2.env)
