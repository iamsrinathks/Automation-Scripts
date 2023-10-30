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
        resources = api_instance.list_namespaced_pod(namespace)
        for resource in resources.items:
            print(f"Pod: {resource.metadata.name}")
        # You can add more resource types here as needed (e.g., Services, Deployments, etc.)
    except Exception as e:
        print(f"Error: {e}")

# Get a list of all namespaces (excluding the excluded ones)
namespace_list = api_instance.list_namespace()
eligible_namespaces = [ns.metadata.name for ns in namespace_list.items if ns.metadata.name not in excluded_namespaces]

# Iterate through the eligible namespaces and list resources
for namespace in eligible_namespaces:
    list_resources_in_namespace(namespace)

print("Resource listing in all eligible namespaces completed.")
