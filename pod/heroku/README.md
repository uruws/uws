# heroku meteor

## update

    uws@janis:~$ cd /srv/uws/deploy
    uws@janis:deploy$ make heroku
    uws@janis:deploy$ export HEROKU_API_KEY=XXXX-XXX-XXX
    uws@janis:deploy$ rm -rf /srv/heroku/download/tapo-beta
    uws@janis:deploy$ ./docker/heroku/cmd.sh slug-update.sh tapo-beta
    uws@janis:deploy$

## build

    uws@janis:deploy$ ./pod/heroku/build.sh tapo-beta

## publish

    uws@janis:deploy$ ./host/ecr-login.sh us-east-2
    uws@janis:deploy$ ./cluster/ecr-push.sh us-east-2 uwspod/heroku uwspod:heroku-20210427

## deploy

    jrms@jaku:Infrastructure$ vim pod/heroku/deploy.yaml
    jrms@jaku:Infrastructure$ git diff pod/heroku/deploy.yaml
    diff --git a/pod/heroku/deploy.yaml b/pod/heroku/deploy.yaml
    index b481d28..1434413 100644
    --- a/pod/heroku/deploy.yaml
    +++ b/pod/heroku/deploy.yaml
    @@ -14,7 +14,7 @@ spec:
             app.kubernetes.io/name: heroku-meteor
         spec:
           containers:
    -        - image: 789470191893.dkr.ecr.us-east-2.amazonaws.com/uwspod:heroku-20210420-5
    +        - image: 789470191893.dkr.ecr.us-east-2.amazonaws.com/uwspod:heroku-20210427
               imagePullPolicy: IfNotPresent
               name: heroku-meteor
               ports:

    jrms@jaku:Infrastructure$ ./eks/admin.sh amybeta
    amybeta@amybeta.us-west-2.eks:~$ ./pod/heroku/deploy.sh secret/tapo-beta.env
