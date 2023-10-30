from kubernetes import client, config

# Set the namespaces you want to exclude from the rolling restart
excluded_namespaces = ["kube-system", "namespace-to-exclude"]  # Add namespaces to exclude here

def list_resources(api_instance, resource_type, namespace=""):
    if namespace:
        resource_list = api_instance.list_namespaced_custom_object("apps", resource_type, namespace)
    else:
        resource_list = api_instance.list_custom_resource("apps", resource_type)

    return resource_list

def perform_rolling_restart(api_instance, namespace):
    # List resources in the specified namespace
    deployments = list_resources(api_instance, "Deployment", namespace)
    statefulsets = list_resources(api_instance, "StatefulSet", namespace)
    daemonsets = list_resources(api_instance, "DaemonSet", namespace)
    pods = api_instance.list_namespaced_pod(namespace)

    # Perform the rolling restart for each deployment, statefulset, and daemonset
    for deployment in deployments.get("items", []):
        deployment_name = deployment["metadata"]["name"]
        print(f"Performing rolling restart for Deployment: {deployment_name} in namespace {namespace}")

        # Trigger a rolling restart for the deployment
        api_instance.patch_namespaced_custom_object("apps", "v1", namespace, "deployments", deployment_name, {"spec": {"template": {"metadata": {"annotations": {"kubectl.kubernetes.io/restartedAt": "now"}}}}})

    for statefulset in statefulsets.get("items", []):
        statefulset_name = statefulset["metadata"]["name"]
        print(f"Performing rolling restart for StatefulSet: {statefulset_name} in namespace {namespace}")

        # Trigger a rolling restart for the statefulset
        api_instance.patch_namespaced_custom_object("apps", "v1", namespace, "statefulsets", statefulset_name, {"spec": {"template": {"metadata": {"annotations": {"kubectl.kubernetes.io/restartedAt": "now"}}}}})

    for daemonset in daemonsets.get("items", []):
        daemonset_name = daemonset["metadata"]["name"]
        print(f"Performing rolling restart for DaemonSet: {daemonset_name} in namespace {namespace}")

        # Trigger a rolling restart for the daemonset
        api_instance.patch_namespaced_custom_object("apps", "v1", namespace, "daemonsets", daemonset_name, {"spec": {"template": {"metadata": {"annotations": {"kubectl.kubernetes.io/restartedAt": "now"}}}}})

def main():
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API client
    api_instance = client.CustomObjectsApi()

    # List all namespaces
    namespaces = api_instance.list_namespace()

    # Confirm with the user before proceeding with the rolling restart
    confirmation = input("Do you want to proceed with the rolling restart? (yes/no): ").strip().lower()
    if confirmation != "yes":
        print("Rolling restart aborted.")
        return

    # Perform a rolling restart for each namespace that is not excluded
    for namespace in namespaces.items:
        if namespace.metadata.name not in excluded_namespaces:
            print(f"Listing resources in namespace: {namespace.metadata.name}")
            perform_rolling_restart(api_instance, namespace.metadata.name)
        else:
            print(f"Skipping namespace: {namespace.metadata.name}")

if __name__ == "__main__":
    main()
