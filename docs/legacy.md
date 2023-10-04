# Legacy Mode

* keep prod environments up and running
    * app.t.o
    * api.t.o
    * prod workers

---

* k8s upgrade: v1.24 being deprecated by AWS at end of December 2023.
    * appc5nxl-2309
    * wrkrc5nxl-2309

---

* cluster migration: move to new platform/owner
    * apptest-2302
    * pnt-2308

---

* uwscli:
    * app-describe
        * to get app/pods describe info (mainly for postmortem)
    * app-logs --previous
        * to show logs output from last restarted pods container
    * app-pm (postmortem)
        * show a last state info summary
        * plus last N lines from previous container log output
