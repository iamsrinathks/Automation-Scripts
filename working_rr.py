from kubernetes import client, config
import datetime

# Define the annotation to add
annotation_key = "kubectl.kubernetes.io/restartedAt"
annotation_value = datetime.datetime.utcnow().isoformat()

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
    # Iterate through namespaces and Deployments
    for namespace in namespace_list.items:
        namespace_name = namespace.metadata.name
        if namespace_name not in excluded_namespaces:
            api_instance = client.AppsV1Api()

            # List Deployments in the current namespace
            deployment_list = api_instance.list_namespaced_deployment(namespace_name)

            for deployment in deployment_list.items:
                deployment_name = deployment.metadata.name
                deployment_namespace = deployment.metadata.namespace

                # Get the current Deployment
                current_deployment = api_instance.read_namespaced_deployment(deployment_name, deployment_namespace)

                # Check if metadata exists, or create it if it doesn't
                if not current_deployment.spec.template.metadata:
                    current_deployment.spec.template.metadata = client.V1ObjectMeta()

                # Check if annotations exist, or create it if it doesn't
                if not current_deployment.spec.template.metadata.annotations:
                    current_deployment.spec.template.metadata.annotations = {}

                # Add or update the annotation
                current_deployment.spec.template.metadata.annotations[annotation_key] = annotation_value

                # Apply the update
                api_instance.patch_namespaced_deployment(deployment_name, deployment_namespace, current_deployment)

    print("Annotations added to Deployments in eligible namespaces.")
