# Project Setups

Document how to install Kubernetes locally

1. Install MicroK8s on Linux

`sudo snap install microk8s --classic`

2. Add your user to the microk8s admin group

`sudo usermod -a -G microk8s $USER`
`sudo chown -f -R $USER ~/.kube`

You will also need to re-enter the session for the group update to take place:

`su - $USER`

3. Check the status while Kubernetes starts

`microk8s status --wait-ready`

4. Turn on the services you want

`microk8s enable dashboard dns ingress`

Try `microk8s enable --help` for a list of available services and optional features. `microk8s disable ‹name›` turns off a service

5. Access the Kubernetes dashboard

`microk8s dashboard-proxy`

6. Start and stop Kubernetes to save battery 

Use `microk8s start` and `microk8s stop` to turn microk8s on and off