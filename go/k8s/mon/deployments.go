// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"encoding/json"
	"net/http"
	"strings"

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
		Replicas int64 `json:"replicas,omitempty"`
	} `json:"spec"`
	Status struct {
		AvailableReplicas  int64             `json:"availableReplicas,omitempty"`
		CurrentReplicas    int64             `json:"currentReplicas,omitempty"`
		Conditions         []statusCondition `json:"conditions,omitempty"`
		ObservedGeneration int64             `json:"observedGeneration"`
		ReadyReplicas      int64             `json:"readyReplicas,omitempty"`
		Replicas           int64             `json:"replicas,omitempty"`
		UpdatedReplicas    int64             `json:"updatedReplicas,omitempty"`
		CurrentNumber      int64             `json:"currentNumberScheduled,omitempty"`
		DesiredNumber      int64             `json:"desiredNumberScheduled,omitempty"`
		NumberAvailable    int64             `json:"numberAvailable,omitempty"`
		NumberMisscheduled int64             `json:"numberMisscheduled,omitempty"`
		NumberReady        int64             `json:"numberReady,omitempty"`
		UpdatedNumber      int64             `json:"updatedNumberScheduled,omitempty"`
	} `json:"status"`
}

type deployList struct {
	ApiVersion string   `json:"apiVersion"`
	Kind       string   `json:"kind"`
	Items      []deploy `json:"items"`
}

var deployCmd string = "get deployments,statefulset,daemonset -A -o json"

func Deployments(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube(strings.Split(deployCmd, " ")...)
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
