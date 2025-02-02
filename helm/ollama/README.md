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

# Install curl

`curl` does not ship with MicroK8s, it is neccessary to install it to ensure you can test the pod from your local machine to talk to the model through the API

1. Run `kubectl exec -n ollama <ollama-podhash> -it -- /bin/sh`

This should drop you into the pod where you can run commands

2. Execute `apt update && apt install -y curl`

# Test Ollama

1. Execute:

    `curl http://localhost:11434/api/generate -d '{`
        `"model": "llama2",`
        `"prompt":"Why is the sky blue?"`
    `}'`

