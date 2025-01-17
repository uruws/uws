AWS_REGION ?= us-east-1
DEPLOY_SERVER ?= janis

.PHONY: default
default: all

.PHONY: clean
clean:
	@rm -rvf ./build ./tmp

.PHONY: distclean
distclean: clean
	@rm -rvf ./docker/golang/build ./docker/golang/tmp
	@rm -rvf ./docker/k8s/build
	@rm -rvf ./docker/k8s/*/build
	@rm -rvf ./docker/uwsbot/build
	@rm -rvf ./docker/uwscli/build
	@rm -rvf ./eks/lib/__pycache__
	@rm -rvf ./srv/crond/build
	@rm -rvf ./srv/munin/build
	@rm -rvf ./srv/munin-node/build

.PHONY: prune
prune:
	@docker system prune -f

#-------------------------------------------------------------------------------
# all

.PHONY: all
all:
	@$(MAKE) bootstrap
	@$(MAKE) devel
	@$(MAKE) clamav
	@$(MAKE) uwsbot
	@$(MAKE) munin
	@$(MAKE) munin-backend
	@$(MAKE) munin-node
	@$(MAKE) proftpd
	@$(MAKE) webapp-all

#-------------------------------------------------------------------------------
# bootstrap

.PHONY: bootstrap
bootstrap:
	@$(MAKE) awscli
	@$(MAKE) base
	@$(MAKE) base-testing
	@$(MAKE) golang
	@$(MAKE) mkcert
	@$(MAKE) acme
	@$(MAKE) k8s
	@$(MAKE) eks
	@$(MAKE) python
	@$(MAKE) ansible
	@$(MAKE) uwscli
	@$(MAKE) mailx
	@$(MAKE) crond
	@$(MAKE) webapp

#-------------------------------------------------------------------------------
# base containers

.PHONY: base
base:
	@./docker/base/build.sh

.PHONY: base-testing
base-testing:
	@./docker/base-testing/build.sh

#-------------------------------------------------------------------------------
# devel

.PHONY: pod-base
pod-base:
	@./pod/base/build.sh

.PHONY: pod-test
pod-test:
	@./pod/test/build.sh

PODTEST_TAG != cat ./pod/test/VERSION

.PHONY: pod-publish
pod-publish:
	@./host/ecr-login.sh us-east-1
	@./cluster/ecr-push.sh us-east-1 uws/pod:test uws:podtest-$(PODTEST_TAG)

.PHONY: devel
devel:
	@./docker/k8s/devel-build.sh
	@./docker/eks/devel-build.sh
	@./docker/asb/devel-build.sh
	@$(MAKE) pod-base
	@$(MAKE) pod-test
	@$(MAKE) heroku

#-------------------------------------------------------------------------------
# utils

.PHONY: utils
utils:
	@$(MAKE) acme

.PHONY: utils-publish
utils-publish:
	@$(MAKE) utils
	@./host/ecr-login.sh sa-east-1
	@./cluster/ecr-push.sh sa-east-1 uws/acme-2309 uwsops:acme

.PHONY: awscli
awscli:
	@./docker/awscli/build.sh

.PHONY: mkcert
mkcert:
	@./docker/mkcert/build.sh

.PHONY: golang
golang:
	@mkdir -vp ./docker/golang/tmp
	@install -v -m 0640 ./go/go.mod ./docker/golang/tmp
	@install -v -m 0640 ./go/go.sum ./docker/golang/tmp
	@./docker/golang/build.sh

.PHONY: python
python:
	@./docker/python/build.sh

.PHONY: uwspkg
uwspkg:
	@./docker/uwspkg/build.sh

.PHONY: acme
acme:
	@./srv/acme/build.sh

.PHONY: clamav
clamav:
	@./docker/clamav/build.sh

.PHONY: proftpd
proftpd:
	@./srv/proftpd/build.sh

.PHONY: ecr-login
ecr-login:
	@./host/ecr-login.sh

.PHONY: ansible
ansible:
	@./docker/asb/build.sh

.PHONY: kali
kali:
	@./srv/kali/build.sh

#-------------------------------------------------------------------------------
# uwscli

.PHONY: uwscli
uwscli:
	@install -v -d -m 0750 ./docker/uwscli/build
	@install -v -C -m 0644 \
		./host/assets/jsbatch/srv/home/uwscli/etc/requirements.txt \
		./docker/uwscli/build/requirements.txt
	@./docker/uwscli/build.sh

#-------------------------------------------------------------------------------
# uwsbot

UWS_BOT_DEPS != find go/bot go/cmd/uwsbot* go/env go/config go/log -type f -name '*.go'

.PHONY: uwsbot
uwsbot: docker/uwsbot/build/uwsbot.bin docker/uwsbot/build/uwsbot-stats.bin docker/uwsbot/build/uwsbot.docs
	@rm -vfr ./docker/uwsbot/build/env/bot
	@mkdir -vp ./docker/uwsbot/build/env/bot/bot
	@install -C -v -m 644 ./go/etc/env/bot/* ./docker/uwsbot/build/env/bot/bot
	@./docker/uwsbot/build.sh

docker/uwsbot/build/uwsbot.bin: docker/golang/build/uwsbot.bin
	@mkdir -vp ./docker/uwsbot/build
	@install -v -C docker/golang/build/uwsbot.bin ./docker/uwsbot/build/uwsbot.bin

docker/golang/build/uwsbot.bin: $(UWS_BOT_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/uwsbot.bin ./cmd/uwsbot

docker/uwsbot/build/uwsbot-stats.bin: docker/golang/build/uwsbot-stats.bin
	@mkdir -vp ./docker/uwsbot/build
	@install -v -C docker/golang/build/uwsbot-stats.bin ./docker/uwsbot/build/uwsbot-stats.bin

docker/golang/build/uwsbot-stats.bin: $(UWS_BOT_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/uwsbot-stats.bin ./cmd/uwsbot-stats

docker/uwsbot/build/uwsbot.docs: $(UWS_BOT_DEPS)
	@mkdir -vp ./docker/uwsbot/build
	@./go/bot/gendocs.sh >./docker/uwsbot/build/uwsbot.docs

.PHONY: uwsbot-devel
uwsbot-devel: docker/uwsbot/build/uwsbot-devel.tgz

docker/uwsbot/build/uwsbot-devel.tgz: docker/uwsbot/build/uwsbot.bin docker/uwsbot/build/uwsbot-stats.bin docker/uwsbot/build/uwsbot.docs
	@rm -rfv ./docker/uwsbot/build/devel
	@mkdir -vp ./docker/uwsbot/build/devel/uws/bin ./docker/uwsbot/build/devel/uws/etc/env/bot
	@(cd ./docker/uwsbot/build \
		&& cp -va env/bot/bot/default env/bot/bot/staging env/bot/bot/stats \
			devel/uws/etc/env/bot/ \
		&& cp -va uwsbot.bin devel/uws/bin/uwsbot \
		&& cp -va uwsbot-stats.bin devel/uws/bin/uwsbot-stats \
		&& tar -cvzf uwsbot-devel.tgz -C devel .)

#-------------------------------------------------------------------------------
# api-job-stats

API_JOB_DEPS != find go/tapo/api go/cmd/api-job-stats go/log -type f -name '*.go'

docker/golang/build/api-job-stats.bin: $(API_JOB_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/api-job-stats.bin ./cmd/api-job-stats

#-------------------------------------------------------------------------------
# mailx

.PHONY: mailx
mailx:
	@./docker/mailx/build.sh

#-------------------------------------------------------------------------------
# crond

.PHONY: crond
crond:
	@./srv/crond/build.sh

#-------------------------------------------------------------------------------
# munin

.PHONY: munin-all
munin-all:
	@$(MAKE) munin
	@$(MAKE) munin-backend
	@$(MAKE) munin-node

.PHONY: munin
munin:
	@mkdir -vp ./srv/munin/build
	@install -v -m 0644 -C ./python/lib/sendmail.py ./srv/munin/build/sendmail.py
	@./srv/munin/build.sh

.PHONY: munin-backend
munin-backend:
	@./srv/munin-backend/build.sh

.PHONY: munin-node
munin-node:
	@./srv/munin-node/build.sh

#-------------------------------------------------------------------------------
# heroku

.PHONY: heroku
heroku:
	@./docker/heroku/build.sh

#-------------------------------------------------------------------------------
# app-stats

APP_STATS_DEPS := go/cmd/app-stats/main.go go/tapo/app/stats/*.go

.PHONY: app-stats
app-stats: docker/golang/build/app-stats.bin

docker/golang/build/app-stats.bin: $(APP_STATS_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/app-stats.bin ./cmd/app-stats

#-------------------------------------------------------------------------------
# webapp

.PHONY: webapp
webapp:
	@./docker/webapp/build.sh

.PHONY: webapp-all
webapp-all:
	@$(MAKE) ab
	@$(MAKE) chatbot
	@$(MAKE) admin

.PHONY: webapp-check
webapp-check:
	@$(MAKE) ab-check
	@$(MAKE) chatbot-check
	@$(MAKE) admin-check

.PHONY: webapp-publish
webapp-publish:
	@$(MAKE) ab-publish
	@$(MAKE) chatbot-publish
	@$(MAKE) admin-publish

#-------------------------------------------------------------------------------
# chatbot

.PHONY: chatbot
chatbot:
	@./srv/chatbot/build.sh

.PHONY: chatbot-check
chatbot-check:
	@./srv/chatbot/check.sh

.PHONY: chatbot-publish
chatbot-publish:
	@$(MAKE) chatbot
	@$(MAKE) chatbot-check
	@./srv/chatbot/publish.sh

#-------------------------------------------------------------------------------
# ab (abench: apache benchmark) (aka uwsab)

.PHONY: ab
ab:
	@./srv/ab/build.sh

.PHONY: ab-check
ab-check:
	@./srv/ab/check.sh

.PHONY: ab-publish
ab-publish:
	@$(MAKE) ab
	@$(MAKE) ab-check
	@./srv/ab/publish.sh

#-------------------------------------------------------------------------------
# admin

.PHONY: admin
admin:
	@./srv/admin/build.sh

.PHONY: admin-check
admin-check:
	@./srv/admin/check.sh

.PHONY: admin-publish
admin-publish:
	@$(MAKE) admin
	@$(MAKE) admin-check
	@./srv/admin/publish.sh

#-------------------------------------------------------------------------------
# deploy

.PHONY: deploy
deploy:
	@echo "i - START deploy `date -R` as ${USER}"
	@$(MAKE) bootstrap
	@$(MAKE) devel
	@$(MAKE) check
	@./host/deploy.sh local $(DEPLOY_SERVER)
	@$(MAKE) prune
	@echo "i - END deploy `date -R`"

#-------------------------------------------------------------------------------
# check

.PHONY: check
check:
	@$(MAKE) check-docker
	@$(MAKE) check-secrets
	@$(MAKE) check-golang
	@$(MAKE) check-cli
	@$(MAKE) check-k8s
	@$(MAKE) check-eks
	@$(MAKE) check-munin
	@$(MAKE) check-munin-node
	@$(MAKE) check-asb
	@$(MAKE) check-awscli
	@$(MAKE) check-webapp

.PHONY: check-docker
check-docker:
	@echo '***** docker/test/run/shellcheck.sh'
	@./docker/check.sh ./test/run/shellcheck.sh

.PHONY: check-golang
check-golang:
	@echo '***** docker/golang/check.sh'
	@./docker/golang/check.sh

.PHONY: check-cli
check-cli:
	@./docker/uwscli/cmd.sh ./test/check.sh

.PHONY: check-k8s
check-k8s:
	@./docker/k8s/devel.sh ./k8s/test/all.sh

.PHONY: check-eks
check-eks:
	@echo '***** eks/test/run/shellcheck.sh'
	@./docker/eks/devel.sh ./eks/test/run/shellcheck.sh
	@echo '***** eks/test/run/coverage.sh'
	@./docker/eks/devel.sh ./eks/test/run/coverage.sh

.PHONY: check-munin
check-munin:
	@./srv/munin/check.sh

.PHONY: check-munin-node
check-munin-node:
	@./srv/munin-node/check.sh ./test/check.sh

.PHONY: check-asb
check-asb:
	@echo '***** asb/test/run/shellcheck.sh'
	@./docker/asb/check.sh ./test/run/shellcheck.sh
	@echo '***** asb/test/run/lint.sh'
	@./docker/asb/check.sh ./test/run/lint.sh

.PHONY: check-awscli
check-awscli:
	@./docker/awscli/check.sh

.PHONY: check-pod-meteor
check-pod-meteor:
	@./pod/meteor/check.sh

.PHONY: check-webapp
check-webapp:
	@$(MAKE) webapp
	@./docker/webapp/self-check.sh

#-------------------------------------------------------------------------------
# uws CA

.PHONY: CA
CA:
	@$(MAKE) mkcert
	@echo '*** ca/ops'
	@$(MAKE) ca/ops
	@echo '*** ca/opstest'
	@$(MAKE) ca/opstest
	@echo '*** ca/smtps'
	@$(MAKE) ca/smtps

.PHONY: ca/ops
ca/ops:
	@./secret/ca/uws/gen.sh ops

.PHONY: ca/opstest
ca/opstest:
	@./secret/ca/uws/gen.sh opstest

.PHONY: ca/smtps
ca/smtps:
	@./secret/ca/uws/gen.sh smtps

#-------------------------------------------------------------------------------
# eks

.PHONY: eks
eks:
	@$(MAKE) k8s
	@./docker/eks/build.sh

#-------------------------------------------------------------------------------
# k8s

.PHONY: k8s
k8s:
	@$(MAKE) k8smon
	@$(MAKE) ngxlogs
	@$(MAKE) hpxlogs
	@./docker/k8s/build.sh

#-------------------------------------------------------------------------------
# k8smon

MON_MUNIN_TAG != cat ./k8s/mon/munin/VERSION

.PHONY: mon-publish
mon-publish:
	@$(MAKE) awscli
	@$(MAKE) munin
	@$(MAKE) munin-backend
	@$(MAKE) munin-node
	@$(MAKE) k8smon-publish
	@$(MAKE) check-munin
	@$(MAKE) check-munin-node
	@./cluster/ecr-push.sh us-east-1 uws/munin-2309 uws:munin-$(MON_MUNIN_TAG)
	@./cluster/ecr-push.sh us-east-1 uws/munin-backend-2309 uws:munin-web-$(MON_MUNIN_TAG)
	@./cluster/ecr-push.sh us-east-1 uws/munin-node-2309 uws:munin-node-$(MON_MUNIN_TAG)

K8SMON_DEPS != find go/cmd/k8smon go/k8s/mon -type f -name '*.go'

.PHONY: k8smon
k8smon: docker/k8s/build/k8smon.bin

docker/k8s/build/k8smon.bin: docker/golang/build/k8smon.bin
	@mkdir -vp ./docker/k8s/build
	@install -v docker/golang/build/k8smon.bin ./docker/k8s/build/k8smon.bin

docker/golang/build/k8smon.bin: $(K8SMON_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/k8smon.bin ./cmd/k8smon

.PHONY: k8smon-publish
k8smon-publish:
	@$(MAKE) k8s
	@$(MAKE) check-k8s
	@./k8s/mon/publish.sh

#-------------------------------------------------------------------------------
# nginx

.PHONY: nginx
nginx:
	@./srv/nginx/build.sh

.PHONY: nginx-check
nginx-check:
	@./srv/nginx/check.sh

.PHONY: nginx-publish
nginx-publish:
	@$(MAKE) nginx
	@$(MAKE) nginx-check
	@./srv/nginx/publish.sh

#-------------------------------------------------------------------------------
# ngxlogs

NGXLOGS_DEPS != find go/cmd/ngxlogs go/ngxlogs -type f -name '*.go'

.PHONY: ngxlogs
ngxlogs: docker/k8s/build/ngxlogs.bin

docker/k8s/build/ngxlogs.bin: docker/golang/build/ngxlogs.bin
	@mkdir -vp ./docker/k8s/build
	@install -v docker/golang/build/ngxlogs.bin ./docker/k8s/build/ngxlogs.bin

docker/golang/build/ngxlogs.bin: $(NGXLOGS_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/ngxlogs.bin ./cmd/ngxlogs

#-------------------------------------------------------------------------------
# hpxlogs

HPXLOGS_DEPS != find go/cmd/hpxlogs go/hpxlogs -type f -name '*.go'

.PHONY: hpxlogs
hpxlogs: docker/k8s/build/hpxlogs.bin

docker/k8s/build/hpxlogs.bin: docker/golang/build/hpxlogs.bin
	@mkdir -vp ./docker/k8s/build
	@install -v docker/golang/build/hpxlogs.bin ./docker/k8s/build/hpxlogs.bin

docker/golang/build/hpxlogs.bin: $(HPXLOGS_DEPS)
	@./docker/golang/cmd.sh build -o /go/build/cmd/hpxlogs.bin ./cmd/hpxlogs

#-------------------------------------------------------------------------------
# publish

.PHONY: publish
publish:
	@$(MAKE) utils-publish
	@$(MAKE) mon-publish
	@$(MAKE) pod-publish
	@$(MAKE) nginx-publish
	@$(MAKE) chatbot-publish
	@$(MAKE) admin-publish

#-------------------------------------------------------------------------------
# secrets

.PHONY: secrets
secrets:
	@./eks/secrets/cluster-all.sh
	@./eks/secrets/uwsadm-update.py
	@./eks/secrets/aws.env-all.sh
	@./eks/secrets/aws.ses-update.py
	@./eks/secrets/tapoS3-all.sh
	@./eks/secrets/uwsasb-update.py

.PHONY: check-secrets
check-secrets:
	@./eks/secrets/check.sh

#-------------------------------------------------------------------------------
# upgrades

.PHONY: upgrades
upgrades:
	@./docker/upgrades-all.sh

.PHONY: upgrades-list
upgrades-list:
	@./docker/upgrades.py

.PHONY: upgrades-check
upgrades-check:
	@./docker/upgrades.py --check
