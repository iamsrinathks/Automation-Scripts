from kubernetes import client, config

# Set the namespaces you want to exclude from listing resources
excluded_namespaces = ["kube-system", "namespace-to-exclude"]  # Add namespaces to exclude here

def list_resources(api_instance, resource_type, namespace=""):
    if namespace:
        resource_list = api_instance.list_namespaced_custom_object("apps", resource_type, namespace)
    else:
        resource_list = api_instance.list_custom_resource("apps", resource_type)

    return resource_list

def main():
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API client
    api_instance = client.CustomObjectsApi()
    v1 = client.CoreV1Api()

    # List all namespaces
    namespaces = v1.list_namespace().items

    # List resources in each namespace that is not excluded
    for namespace in namespaces:
        if namespace.metadata.name not in excluded_namespaces:
            print(f"Listing resources in namespace: {namespace.metadata.name}")

            # List your desired resources here, e.g., Deployments, StatefulSets, DaemonSets
            deployments = list_resources(api_instance, "Deployment", namespace.metadata.name)
            statefulsets = list_resources(api_instance, "StatefulSet", namespace.metadata.name)
            daemonsets = list_resources(api_instance, "DaemonSet", namespace.metadata.name)
            pods = api_instance.list_namespaced_pod(namespace.metadata.name)

            # Process and print the resources as needed
            # You can iterate through deployments, statefulsets, daemonsets, or pods
            # and perform actions based on your requirements.

        else:
            print(f"Skipping namespace: {namespace.metadata.name}")

if __name__ == "__main__":
    main()











from kubernetes import client, config

# Set the namespaces you want to exclude from the rolling restart
excluded_namespaces = ["kube-system", "namespace-to-exclude"]  # Add namespaces to exclude here

def perform_rolling_restart(api_instance, namespace):
    # List resources in the specified namespace
    # You can adapt the following code to trigger a rolling restart for resources in the namespace.

def main():
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API client
    api_instance = client.CustomObjectsApi()
    v1 = client.CoreV1Api()

    # List all namespaces
    namespaces = v1.list_namespace().items

    # Perform a rolling restart for each namespace that is not excluded
    for namespace in namespaces:
        if namespace.metadata.name not in excluded_namespaces:
            print(f"Performing rolling restart in namespace: {namespace.metadata.name}")
            perform_rolling_restart(api_instance, namespace.metadata.name)
        else:
            print(f"Skipping namespace: {namespace.metadata.name}")

if __name__ == "__main__":
    main()
