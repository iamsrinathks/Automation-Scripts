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



---------

import subprocess

# Define the excluded namespaces
excluded_namespaces = ["kube-system", "default", "excluded-namespace-1", "excluded-namespace-2"]

# Get a list of all namespaces
all_namespaces = subprocess.check_output("kubectl get namespaces -o custom-columns=NAME:.metadata.name --no-headers", shell=True).decode("utf-8").split()

# Determine eligible namespaces by excluding the ones in the exclusion list
eligible_namespaces = [ns for ns in all_namespaces if ns not in excluded_namespaces]

# Define the Deployment name
deployment_name = "your-deployment-name"

# Iterate through the eligible namespaces and perform rolling restart
for namespace in eligible_namespaces:
    subprocess.call(f"kubectl rollout restart deployment/{deployment_name} -n {namespace}", shell=True)

