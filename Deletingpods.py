from kubernetes import client, config

# Set the namespaces you want to exclude
excluded_namespaces = ["kube-system", "default"]

# Initialize the Kubernetes configuration
config.load_kube_config()  # Loads the default kubeconfig file

# Create a Kubernetes API client
api_instance = client.CoreV1Api()

# List all namespaces
namespaces = api_instance.list_namespace()

# Iterate through namespaces and delete pods in non-excluded namespaces
for namespace in namespaces.items:
    if namespace.metadata.name not in excluded_namespaces:
        try:
            # List pods in the current namespace
            pods = api_instance.list_namespaced_pod(namespace.metadata.name)
            for pod in pods.items:
                print(f"Deleting pod: {pod.metadata.name} in namespace: {namespace.metadata.name}")
                api_instance.delete_namespaced_pod(pod.metadata.name, namespace.metadata.name)
                print(f"Deleted pod: {pod.metadata.name} in namespace: {namespace.metadata.name}")
        except Exception as e:
            print(f"Failed to delete pods in namespace {namespace.metadata.name}: {str(e)}")
    else:
        print(f"Skipping namespace: {namespace.metadata.name}")

print("Pod deletion completed.")
