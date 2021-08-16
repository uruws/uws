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
	Kind string `json:"kind"`
	Meta struct {
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

func nodesReport() *stats.Parser {
	p := stats.NewParser("nodes")
	out, err := Kube("get", "nodes", "-o", "json")
	if err != nil {
		log.Error("get nodes: %s", err)
		p.SetError()
		return p
	}
	nl := new(nodeList)
	if err := json.Unmarshal(out, &nl); err != nil {
		log.Error("read nodes: %s", err)
		p.SetError()
		return p
	}
	// nodes
	p.Set("nodes_total", int64(len(nl.Items)))
	p.Add("nodes_type")
	// conditions
	p.Set("memory_pressure", 0)
	p.Set("disk_pressure", 0)
	p.Set("pid_pressure", 0)
	p.Set("ready_condition", 0)
	p.Set("unknown_condition", 0)
	for _, n := range nl.Items {
		// type
		ntype := n.Meta.Labels["node.kubernetes.io/instance-type"]
		if ntype == "" {
			ntype = n.Meta.Labels["beta.kubernetes.io/instance-type"]
		}
		if ntype == "" {
			ntype = "unknown"
		}
		p.ChildInc("nodes_type", ntype)
		// conditions
		condFound := false
		for _, cond := range n.Status.Conditions {
			if cond.Type == "MemoryPressure" && cond.Status == "True" {
				p.Inc("memory_pressure")
				condFound = true
			}
			if cond.Type == "DiskPressure" && cond.Status == "True" {
				p.Inc("disk_pressure")
				condFound = true
			}
			if cond.Type == "PIDPressure" && cond.Status == "True" {
				p.Inc("pid_pressure")
				condFound = true
			}
			if cond.Type == "Ready" && cond.Status == "True" {
				p.Inc("ready_condition")
				condFound = true
			}
		}
		if !condFound {
			p.Inc("unknown_condition")
		}
	}
	return p
}

func NodesConfig(w http.ResponseWriter, r *http.Request) {
	log.Debug("nodes config")
	start := wapp.Start()

	buf := stats.NewBuffer()
	defer buf.Reset()

	// parse report
	rpt := nodesReport()

	// nodes
	nodes := stats.NewConfig("nodes")
	nodes.Title = Cluster() + " nodes"
	nodes.VLabel = "number"
	nodes.Category = "node"
	nodes.Printf = "%3.0lf"
	// number
	nTotal := nodes.AddField("f00_total")
	nTotal.Label = "nodes"
	nTotal.Draw = "AREASTACK"
	// types
	for _, t := range rpt.ChildList("nodes_type") {
		f := nodes.AddField(stats.CleanFN(t))
		f.Label = t
		f.Draw = "AREASTACK"
	}
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

	// cache report
	if !rpt.HasError() {
		stats.CacheSet(rpt)
	}

	wapp.Write(w, r, start, "%s", buf)
}

func Nodes(w http.ResponseWriter, r *http.Request) {
	log.Debug("nodes report")
	start := wapp.Start()

	buf := stats.NewBuffer()
	defer buf.Reset()

	// parse report
	rpt := stats.CacheGet("nodes")
	if rpt == nil {
		rpt = nodesReport()
	}

	// nodes
	nodes := stats.NewReport("nodes")
	// total
	nodesTotal := nodes.AddField("f00_total")
	nodesTotal.Value = rpt.Get("nodes_total")
	// types
	for _, t := range rpt.ChildList("nodes_type") {
		f := nodes.AddField(stats.CleanFN(t))
		f.Value = rpt.ChildGet("nodes_type", t)
	}
	buf.Write("%s", nodes)

	// nodes condition
	nc := stats.NewReport("nodes_condition")
	// unknown condition
	ncUnknown := nc.AddField("f00_unknown")
	ncUnknown.Value = rpt.Get("unknown_condition")
	// memory pressure condition
	ncMem := nc.AddField("f01_memory_pressure")
	ncMem.Value = rpt.Get("memory_pressure")
	// disk pressure condition
	ncDisk := nc.AddField("f02_disk_pressure")
	ncDisk.Value = rpt.Get("disk_pressure")
	// pid pressure condition
	ncPID := nc.AddField("f03_pid_pressure")
	ncPID.Value = rpt.Get("pid_pressure")
	// ready condition
	ncReady := nc.AddField("f04_ready")
	ncReady.Value = rpt.Get("ready_condition")
	buf.Write("%s", nc)

	wapp.Write(w, r, start, "%s", buf)
}
