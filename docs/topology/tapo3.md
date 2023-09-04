# tapo topology (v3)

                        User
                         |
                         |
                        ALB (AWS Application Load Balancer) (TLS Termination)
                         |
                         |
     ----------------------------------------------------- Kubernetes cluster
     |      |            |            |            |        |
     |   .........    .........    .........    .........   |
     |   . nginx .    . nginx .    . nginx .    . nginx .   | (TLS termination)
     |   .........    .........    .........    .........   |
     |      |            |            |            |        |
     |      |            |            |            |        |
     |    .......      .......      .......      .......    |
     |    . App .      . App .      . App .      . App .    |
     |    .......      .......      .......      .......    |
     |                                                      |
     --------------------------------------------------------

## Description

* Using an Application load balancer (layer 7)
      * It can take decisions based on application level information (like HTTP headers, URL and such)
      * So we can use an WAF service

* Equal number of nginx replicas and App replicas

* One on one nginx and App communication

* TLS termination has to be done in both sides
      * ALB and nginx
      * So we encrypt traffic between ALB and nginx too (as it's a public network)
