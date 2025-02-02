# Helm Projects

# Project Setup

The following directions will help get MicroK8s and Helm running on your local machine to host Ollama or any other application on MicroK8s

These 

# MicroK8s

Document how to install MicroK8s locally and view the Kubernets Dashboard

1. Install MicroK8s on Linux

    `sudo snap install microk8s --classic`

2. Add your user to the MicroK8s admin group

    `sudo usermod -a -G microk8s $USER` \
    `sudo chown -f -R $USER ~/.kube`

3. You will also need to re-enter the session for the group update to take place

    `su - $USER`

4. Check the status while MicroK8s starts

    `MicroK8s status --wait-ready`

5. Turn on the services you want

    `microk8s enable dashboard dns ingress`

    Try `microk8s enable --help` for a list of available services and optional features. `microk8s disable ‹name›` turns off a service

6. Access the MicroK8s dashboard

    `microk8s dashboard-proxy`

7. Start and stop MicroK8s to save battery 

    Use `microk8s start` and `microk8s stop` to turn MicroK8s on and off

8. View the MicroK8s-dashboard
    
    Use this token in the https login UI of the MicroK8s-dashboard service.

    `microk8s kubectl describe secret -n kube-system microk8s-dashboard-token`

# Helm

Document how to install Helm to manage deployment of resources to the MicroK8s cluster

1. Use curl to pull down Helm

    `curl -O https://get.helm.sh/helm-v3.16.2-linux-amd64.tar.gz`

2. Unpack the file

    `tar xvf helm-v3.16.2-linux-amd64.tar.gz`

3. Move the linux-amd64/helm file to the /usr/local/bin directory:

    `sudo mv linux-amd64/helm /usr/local/bin`

4. Remove the downloaded file using the following command:

    `rm helm-v3.16.2-linux-amd64.tar.gz`

5. Finally, verify you installed Helm by checking the version of the software:

    `helm version`

    The terminal should print out the version of Helm that is installed