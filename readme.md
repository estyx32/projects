# Project Setups

# Kubernetes

Document how to install Kubernetes locally and view the Kubernets Dashboard

1. Install MicroK8s on Linux

    `sudo snap install microk8s --classic`

2. Add your user to the microk8s admin group

    `sudo usermod -a -G microk8s $USER` \
    `sudo chown -f -R $USER ~/.kube`

3. You will also need to re-enter the session for the group update to take place

    `su - $USER`

4. Check the status while Kubernetes starts

    `microk8s status --wait-ready`

5. Turn on the services you want

    `microk8s enable dashboard dns ingress`

    Try `microk8s enable --help` for a list of available services and optional features. `microk8s disable ‹name›` turns off a service

6. Access the Kubernetes dashboard

    `microk8s dashboard-proxy`

7. Start and stop Kubernetes to save battery 

    Use `microk8s start` and `microk8s stop` to turn microk8s on and off

# Viewing the kubernetes-dashboard
Use this token in the https login UI of the kubernetes-dashboard service.

`microk8s kubectl describe secret -n kube-system microk8s-dashboard-token`

# Create a namespace for the deployment

1. kubectl create namespace <namespace-name>

    You can also manage this with a YAML file (recomended)

`apiVersion: v1`
`kind: Namespace`
`metadata:`
  `name: <namespace-name>`