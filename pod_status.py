from kubernetes import client, config

# Define namespaces to exclude
excluded_namespaces = ["kube-system", "default", "excluded-namespace-1", "excluded-namespace-2"]

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.CoreV1Api()

# List all namespaces
namespace_list = api_client.list_namespace()
if not namespace_list:
    print("No namespaces found.")
else:
    # Iterate through namespaces
    for namespace in namespace_list.items:
        namespace_name = namespace.metadata.name
        if namespace_name not in excluded_namespaces:
            print(f"Status of Pods in Namespace: {namespace_name}")
            pod_list = api_client.list_namespaced_pod(namespace_name)

            for pod in pod_list.items:
                print(f"Pod: {pod.metadata.name}")
                print(f"  Phase: {pod.status.phase}")
                print(f"  Conditions: {pod.status.conditions}")
                print("")

            print("=============================")
