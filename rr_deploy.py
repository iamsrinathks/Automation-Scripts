from kubernetes import dynamic, config
from kubernetes.client import api_client
import datetime

# Define excluded namespaces
excluded_namespaces = ["kube-system", "default", "excluded-namespace-1", "excluded-namespace-2"]

# Load Kubernetes configuration
config.load_kube_config()

# Create a dynamic client
client = dynamic.DynamicClient(api_client.ApiClient())

# Get a reference to the Deployment resource
api = client.resources.get(api_version="apps/v1", kind="Deployment")

# Retrieve the list of all namespaces
all_namespaces = client.resources.get(api_version="v1", kind="Namespace").get()

# Iterate through all namespaces and patch the Deployment in eligible namespaces
for ns in all_namespaces.items:
    namespace = ns.metadata.name
    if namespace not in excluded_namespaces:
        deployment_manifest = api.get(name=deployment_name, namespace=namespace).to_dict()
        deployment_manifest["spec"]["template"]["metadata"]["annotations"] = {
            "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow().isoformat()
        }
        api.patch(body=deployment_manifest, name=deployment_name, namespace=namespace)
