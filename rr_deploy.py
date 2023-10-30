from kubernetes import dynamic, config
import datetime
from kubernetes.client import api_client

# Define excluded namespaces
excluded_namespaces = ["kube-system", "default", "excluded-namespace-1", "excluded-namespace-2"]

# Load Kubernetes configuration
config.load_kube_config()

# Create a dynamic client with the api_client
client = dynamic.DynamicClient(api_client.ApiClient())

# Retrieve the list of all namespaces
all_namespaces = client.resources.get(api_version="v1", kind="Namespace").get()

# Iterate through all namespaces
for ns in all_namespaces.items:
    namespace = ns.metadata.name
    if namespace not in excluded_namespaces:
        # Get a reference to Deployments in the current namespace
        deployments = client.resources.get(api_version="apps/v1", kind="Deployment", namespace=namespace).get()

        # Iterate through Deployments in the current namespace and patch each one
        for deployment in deployments.items:
            deployment_name = deployment.metadata.name
            deployment_manifest = client.resources.get(api_version="apps/v1", kind="Deployment", namespace=namespace, name=deployment_name).get().to_dict()
            deployment_manifest["spec"]["template"]["metadata"]["annotations"] = {
                "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow().isoformat()
            }
            client.resources.get(api_version="apps/v1", kind="Deployment", namespace=namespace, name=deployment_name).patch(body=deployment_manifest)
