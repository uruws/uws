// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"encoding/json"
	"net/http"

	"uws/log"
	"uws/wapp"
)

type nodeInfo struct {
	VolumeEBS   string `json:"attachable-volumes-aws-ebs"`
	CPU         string `json:"cpu"`
	Storage     string `json:"ephemeral-storage"`
	HugePages1G string `json:"hugepages-1Gi"`
	HugePages2M string `json:"hugepages-2Mi"`
	Memory      string `json:"memory"`
	Pods        string `json:"pods"`
}

type nodeCondition struct {
	Status string `json:"status"`
	Type   string `json:"type"`
}

type nodeImages struct {
	Names     []string `json:"names"`
	SizeBytes int      `json:"sizeBytes"`
}

type node struct {
	Kind     string `json:"kind"`
	Metadata struct {
		Labels          map[string]string `json:"labels"`
		Name            string            `json:"name"`
		ResourceVersion string            `json:"resourceVersion"`
		UID             string            `json:"uid"`
	} `json:"metadata"`
	Status struct {
		Allocatable nodeInfo        `json:"allocatable"`
		Capacity    nodeInfo        `json:"capacity"`
		Conditions  []nodeCondition `json:"conditions"`
		Images      []nodeImages    `json:"images"`
		NodeInfo    struct {
			Arch             string `json:"architecture"`
			ContainerRuntime string `json:"containerRuntimeVersion"`
			Kernel           string `json:"kernelVersion"`
			KubeProxy        string `json:"kubeProxyVersion"`
			Kubelet          string `json:"kubeletVersion"`
			ID               string `json:"machineID"`
			OS               string `json:"operatingSystem"`
			System           string `json:"osImage"`
			UUID             string `json:"systemUUID"`
		} `json:"nodeInfo"`
	} `json:"status"`
}

type nodeList struct {
	ApiVersion string `json:"apiVersion"`
	Kind       string `json:"kind"`
	Items      []node `json:"items"`
}

func NodesConfig(w http.ResponseWriter, r *http.Request) {
	log.Debug("nodes config")
	start := wapp.Start()
	cluster := CleanFN(Cluster())
	buf := NewBuffer()
	buf.Write("multigraph %s_nodes\n", cluster)
	wapp.Write(w, r, start, "%s", buf.String())
}

func Nodes(w http.ResponseWriter, r *http.Request) {
	log.Debug("nodes report")
	start := wapp.Start()
	out, err := Kube("get", "nodes", "-o", "json")
	if err != nil {
		wapp.Error(w, r, start, err)
		return
	}
	nl := new(nodeList)
	if err := json.Unmarshal(out, &nl); err != nil {
		wapp.Error(w, r, start, err)
		return
	}
	buf := NewBuffer()
	buf.Write("%d\n", len(nl.Items))
	wapp.Write(w, r, start, "%s", buf.String())
}
