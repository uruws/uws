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

type nodeImages struct {
	Names     []string `json:"names"`
	SizeBytes int      `json:"sizeBytes"`
}

type node struct {
	Kind string `json:"kind"`
	Meta struct {
		Labels          map[string]string `json:"labels"`
		Name            string            `json:"name"`
		ResourceVersion string            `json:"resourceVersion"`
		UID             string            `json:"uid"`
	} `json:"metadata"`
	Status struct {
		Allocatable nodeInfo          `json:"allocatable"`
		Capacity    nodeInfo          `json:"capacity"`
		Conditions  []statusCondition `json:"conditions"`
		Images      []nodeImages      `json:"images"`
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

func Nodes(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube("get", "nodes", "-o", "json")
	if err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	nl := new(nodeList)
	if err := json.Unmarshal(out, &nl); err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	wapp.WriteJSON(w, r, start, &nl)
}
