# tapo topology (v2)

             User
              |
              |
             NLB (AWS Network Load Balancer)
              |
              |
       -------------------------------- Kubernetes cluster
       |      |                          |
       |   ...........................   |
       |   . nginx nginx nginx nginx .   | (TLS termination)
       |   ...........................   |
       |      |     |     |     |        |
       |      |     |     |     |        |
       |   .........................     |
       |   . App   App   App   App .     |
       |   .........................     |
       |                                 |
       -----------------------------------

## Description

* Using a Network load balancer (layer 3)
    * It only knows about IP addresses and port numbers

* Equal number of nginx replicas and App replicas

* Any nginx can talk with any App

* TLS termination done at nginx level
