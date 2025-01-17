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

type containerLastState struct {
	Terminated struct {
		Reason string `json:"reason"`
	} `json:"terminated"`
}

type containerStatus struct {
	Name         string             `json:"name"`
	Image        string             `json:"image"`
	Ready        bool               `json:"ready"`
	RestartCount int64              `json:"restartCount"`
	Started      bool               `json:"started"`
	LastState    containerLastState `json:"lastState,omitempty"`
}

type pod struct {
	Kind string `json:"kind"`
	Meta struct {
		Name            string `json:"name"`
		Namespace       string `json:"namespace"`
		ResourceVersion string `json:"resourceVersion"`
		UID             string `json:"uid"`
		GenerateName    string `json:"generateName"`
		Labels          struct {
			PodTplHash string `json:"pod-template-hash"`
		} `json:"labels"`
	} `json:"metadata"`
	Spec struct {
		Containers []containerStatus `json:"containers"`
	} `json:"spec"`
	Status struct {
		Conditions []statusCondition `json:"conditions,omitempty"`
		Containers []containerStatus `json:"containerStatuses,omitempty"`
		Phase      string            `json:"phase"`
	} `json:"status"`
}

type podList struct {
	ApiVersion string `json:"apiVersion"`
	Kind       string `json:"kind"`
	Items      []pod  `json:"items"`
}

var podsCmd string = "get pods -A -o json"

func Pods(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube(strings.Split(podsCmd, " ")...)
	if err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	pl := new(podList)
	if err := json.Unmarshal(out, &pl); err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	wapp.WriteJSON(w, r, start, &pl)
}
