from kubernetes import client, config

# Define the namespaces to be excluded from the rolling restart
excluded_namespaces = ["kube-system", "default"]

# Load Kubernetes configuration from the default location
config.load_kube_config()

# Create a Kubernetes API instance for working with Deployments
api_instance = client.AppsV1Api()

# Define the resource type you want to restart (e.g., "Deployment" or "StatefulSet")
resource_type = "Deployment"

# Function to perform a rolling restart in a namespace
def rolling_restart(namespace):
    print(f"Performing a rolling restart in the {namespace} namespace...")
    try:
        # Get a list of resources in the namespace
        resources = api_instance.list_namespaced_deployment(namespace)
        for resource in resources.items:
            api_instance.patch_namespaced_deployment_scale(name=resource.metadata.name, namespace=namespace, body={"spec": {"replicas": resource.spec.replicas}})
        print(f"Rolling restart in the {namespace} namespace completed.")
    except Exception as e:
        print(f"Error: {e}")

# Get a list of all namespaces (excluding the excluded ones)
v1 = client.CoreV1Api()
namespace_list = v1.list_namespace()
eligible_namespaces = [ns.metadata.name for ns in namespace_list.items if ns.metadata.name not in excluded_namespaces]

# Iterate through the eligible namespaces and perform rolling restarts
for namespace in eligible_namespaces:
    rolling_restart(namespace)

print("Rolling restarts in all eligible namespaces completed.")
