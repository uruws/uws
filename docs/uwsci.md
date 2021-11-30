# uws continuous integration

Continuous integration setup.

The CI scripts are run in the following order:

    .ci/build.sh
    .ci/check.sh
    .ci/install.sh
    .ci/deploy.sh
    .ci/clean.sh

It's OK if they don't exist.

If any of them fails, CI is aborted and a rollback to previous version is
dispatched.

If you need to change the `.ci` directory, you can create `.uwsci.conf` as
follows:

    [deploy]
    ci_dir = continuous-integration

The directory can't be outside of the repository tree.
