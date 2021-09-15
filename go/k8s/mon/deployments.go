// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"encoding/json"
	"net/http"

	"uws/log"
	"uws/wapp"
)

type deploy struct {
	Kind string `json:"kind"`
	Meta struct {
		Name            string `json:"name"`
		Namespace       string `json:"namespace"`
		Generation      int64  `json:"generation"`
		ResourceVersion string `json:"resourceVersion"`
		UID             string `json:"uid"`
	} `json:"metadata"`
	Spec struct {
		Replicas int64 `json:"replicas"`
	} `json:"spec"`
	Status struct {
		AvailableReplicas  int64             `json:"availableReplicas"`
		Conditions         []statusCondition `json:"conditions"`
		ObservedGeneration int64             `json:"observedGeneration"`
		ReadyReplicas      int64             `json:"readyReplicas"`
		Replicas           int64             `json:"replicas"`
		UpdatedReplicas    int64             `json:"updatedReplicas"`
	} `json:"status"`
}

type deployList struct {
	ApiVersion string   `json:"apiVersion"`
	Kind       string   `json:"kind"`
	Items      []deploy `json:"items"`
}

func Deployments(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube("get", "deployments", "-A", "-o", "json")
	if err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	nl := new(deployList)
	if err := json.Unmarshal(out, &nl); err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	wapp.WriteJSON(w, r, start, &nl)
}
