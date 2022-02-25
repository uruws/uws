# Authentication and authorization

OS users, groups and tools permissions are managed from [uwscli](../../host/assets/jsbatch/uws/init/01-uwscli) deploy script.

There are three different levels of access:

* user
    * *read* access to *authorized* apps only
    * can get logs and such actions
    * no deploy nor any disruptive action

* operator
    * *read/write* access to *authorized* apps only
    * can do deploys and such actions

* admin
    * can take *any* action to *all* apps
