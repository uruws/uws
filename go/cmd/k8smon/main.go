// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements k8smon util.
package main

import (
	"net/http"
	"os"

	"uws/k8s/mon"
	"uws/log"
	"uws/wapp"
)

var (
	cluster        string
	listenAndServe func(string, http.Handler) error
	osHostname     func() (string, error)
)

func init() {
	cluster = mon.Cluster()
	listenAndServe = http.ListenAndServe
	osHostname = os.Hostname
}

func main() {
	log.Init("k8smon")
	log.Debug("main init")

	if cluster == "" {
		log.Fatal("UWS_CLUSTER not set")
	}
	log.Debug("cluster %s", cluster)

	// internal endpoint for k8s check
	http.HandleFunc("/_/healthz", healthzHandler)

	// haproxy URLs scheme
	http.HandleFunc("/k8smon/_/ping", pingHandler)
	http.HandleFunc("/k8smon/kube/nodes", mon.Nodes)
	http.HandleFunc("/k8smon/kube/deployments", mon.Deployments)
	http.HandleFunc("/k8smon/kube/pods", mon.Pods)
	http.HandleFunc("/k8smon/kube/top_nodes", mon.TopNodes)
	http.HandleFunc("/k8smon/kube/top_pods", mon.TopPods)
	http.HandleFunc("/k8smon/kube/k8s_metrics", mon.K8s)
	http.HandleFunc("/k8smon/", mainHandler)

	// nginx URLs scheme
	http.HandleFunc("/_/ping", pingHandler)
	http.HandleFunc("/kube/nodes", mon.Nodes)
	http.HandleFunc("/kube/deployments", mon.Deployments)
	http.HandleFunc("/kube/pods", mon.Pods)
	http.HandleFunc("/kube/top_nodes", mon.TopNodes)
	http.HandleFunc("/kube/top_pods", mon.TopPods)
	http.HandleFunc("/kube/k8s_metrics", mon.K8s)
	http.HandleFunc("/", mainHandler)

	log.Debug("serve...")
	log.Fatal("%s", listenAndServe(":2800", nil))
}

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if _, err := osHostname(); err != nil {
		wapp.Error(w, r, start, err)
	} else {
		wapp.Write(w, r, start, "ok\n")
	}
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if hostname, err := osHostname(); err != nil {
		wapp.Error(w, r, start, err)
	} else {
		wapp.Write(w, r, start, "mon@%s\n", hostname)
	}
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if r.URL.Path != "/" {
		wapp.NotFound(w, r, start)
	} else {
		wapp.Write(w, r, start, "index\n")
	}
}
