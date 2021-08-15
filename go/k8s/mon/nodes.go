// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"encoding/json"
	"net/http"

	"uws/k8s/mon/stats"
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

	buf := stats.NewBuffer()
	defer buf.Reset()

	// nodes number
	nodes := stats.NewConfig("nodes")
	nodes.Title = Cluster() + " nodes"
	nodes.VLabel = "number"
	nodes.Category = "node"
	nodes.Printf = "%3.0lf"
	nTotal := nodes.AddField("f00_total")
	nTotal.Label = "nodes"
	nTotal.Draw = "AREASTACK"
	buf.Write("%s", nodes)

	// nodes conditions
	nc := stats.NewConfig("nodes_condition")
	nc.Title = Cluster() + " nodes condition"
	nc.VLabel = "number"
	nc.Total = "total"
	nc.Category = "node"
	nc.Printf = "%3.0lf"
	// unknown condition
	ncUnknown := nc.AddField("f00_unknown")
	ncUnknown.Label = "unknown"
	ncUnknown.Draw = "AREASTACK"
	// memory pressure condition
	ncMem := nc.AddField("f01_memory_pressure")
	ncMem.Label = "memory pressure"
	ncMem.Draw = "AREASTACK"
	// disk pressure condition
	ncDisk := nc.AddField("f02_disk_pressure")
	ncDisk.Label = "disk pressure"
	ncDisk.Draw = "AREASTACK"
	// pid pressure condition
	ncPID := nc.AddField("f03_pid_pressure")
	ncPID.Label = "pid pressure"
	ncPID.Draw = "AREASTACK"
	// ready condition
	ncReady := nc.AddField("f04_ready")
	ncReady.Label = "ready"
	ncReady.Draw = "AREASTACK"
	buf.Write("%s", nc)

	wapp.Write(w, r, start, "%s", buf)
}

type nodesReport struct {
	UnknownCondition int64
	MemoryPressure   int64
	DiskPressure     int64
	PIDPressure      int64
	ReadyCondition   int64
}

func (r *nodesReport) Parse(nl *nodeList) {
	for _, n := range nl.Items {
		// conditions
		condFound := false
		for _, cond := range n.Status.Conditions {
			if cond.Type == "MemoryPressure" && cond.Status == "True" {
				r.MemoryPressure += 1
				condFound = true
			}
			if cond.Type == "DiskPressure" && cond.Status == "True" {
				r.DiskPressure += 1
				condFound = true
			}
			if cond.Type == "PIDPressure" && cond.Status == "True" {
				r.PIDPressure += 1
				condFound = true
			}
			if cond.Type == "Ready" && cond.Status == "True" {
				r.ReadyCondition += 1
				condFound = true
			}
		}
		if !condFound {
			r.UnknownCondition += 1
		}
	}
}

func Nodes(w http.ResponseWriter, r *http.Request) {
	log.Debug("nodes report")
	start := wapp.Start()

	var hasError bool
	out, err := Kube("get", "nodes", "-o", "json")
	if err != nil {
		log.Error("get nodes: %s", err)
		hasError = true
	}

	nl := new(nodeList)
	if !hasError {
		if err := json.Unmarshal(out, &nl); err != nil {
			log.Error("read nodes: %s", err)
			hasError = true
		}
	}

	buf := stats.NewBuffer()
	defer buf.Reset()

	// nodes number
	nodes := stats.NewReport("nodes")
	nodesTotal := nodes.AddField("f00_total")
	if hasError {
		nodesTotal.Unknown = true
		wapp.Write(w, r, start, "%s", nodes)
		return
	}
	nodesTotal.Value = int64(len(nl.Items))
	buf.Write("%s", nodes)

	// parse report
	rpt := new(nodesReport)
	rpt.Parse(nl)

	// nodes condition
	nc := stats.NewReport("nodes_condition")
	// unknown condition
	ncUnknown := nc.AddField("f00_unknown")
	ncUnknown.Value = rpt.UnknownCondition
	// memory pressure condition
	ncMem := nc.AddField("f01_memory_pressure")
	ncMem.Value = rpt.MemoryPressure
	// disk pressure condition
	ncDisk := nc.AddField("f02_disk_pressure")
	ncDisk.Value = rpt.DiskPressure
	// pid pressure condition
	ncPID := nc.AddField("f03_pid_pressure")
	ncPID.Value = rpt.PIDPressure
	// ready condition
	ncReady := nc.AddField("f04_ready")
	ncReady.Value = rpt.ReadyCondition
	buf.Write("%s", nc)

	wapp.Write(w, r, start, "%s", buf)
}
