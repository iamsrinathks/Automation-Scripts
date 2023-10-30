from kubernetes import client, config

# Define the namespaces to be excluded from the listing
excluded_namespaces = ["kube-system", "default"]

# Load Kubernetes configuration from the default location
config.load_kube_config()

# Create a Kubernetes API client
api_instance = client.CoreV1Api()

# Function to list resources in a namespace
def list_resources_in_namespace(namespace):
    print(f"Resources in the {namespace} namespace:")
    try:
        # List Pods
        pods = api_instance.list_namespaced_pod(namespace)
        for pod in pods.items:
            print(f"Pod: {pod.metadata.name}")

        # List Services
        services = api_instance.list_namespaced_service(namespace)
        for service in services.items:
            print(f"Service: {service.metadata.name}")

        # List Deployments (or other resource types)
        apps_api_instance = client.AppsV1Api()
        deployments = apps_api_instance.list_namespaced_deployment(namespace)
        for deployment in deployments.items:
            print(f"Deployment: {deployment.metadata.name}")

        # You can add more resource types here as needed

    except Exception as e:
        print(f"Error: {e}")

# Get a list of all namespaces (excluding the excluded ones)
namespace_list = api_instance.list_namespace()
eligible_namespaces = [ns.metadata.name for ns in namespace_list.items if ns.metadata.name not in excluded_namespaces]

# Iterate through the eligible namespaces and list resources
for namespace in eligible_namespaces:
    list_resources_in_namespace(namespace)

print("Resource listing in all eligible namespaces completed.")
