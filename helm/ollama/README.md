# Ollama Setup

1. Create a `deployment.yaml`, `service.yaml` for    the Ollama service, and a `namespace.yaml` for the Ollama namespace

2. Create the Ollama namespace
    
    `microkb8s kubectl create namespace ollama`

3. Apply the Ollama deployment

    `microk8s kubectl apply -f deployment.yaml`

4. Verify the deployment was applied

    `kubectl get deployments -n ollama`

5. Ensure the pods are running

    `kubectl get pods -n ollama`

6. Create a service to expose the Ollama application

    `microk8s kubectl apply -f service.yaml`

7.  Forward localhost:11434 requests to port 80

    `microk8s kubectl -n ollama port-forward service/ollama 11434:80`

8. Visit `http://localhost:11434/`, you should see "Ollama is running" on the webpage

