from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.CoreV1Api()

# Create a Kubernetes API client for Deployments
deployment_api = client.AppsV1Api()

# Define the annotation to add
annotation_key = "kubectl.kubernetes.io/restartedAt"
annotation_value = datetime.datetime.utcnow().isoformat()

# Define namespaces to exclude
excluded_namespaces = ["kube-system", "default", "excluded-namespace-1", "excluded-namespace-2"]

# List all namespaces
namespace_list = api_client.list_namespace()
if not namespace_list:
    print("No namespaces found.")
else:
    # Iterate through namespaces and Deployments
    for namespace in namespace_list.items:
        namespace_name = namespace.metadata.name
        if namespace_name not in excluded_namespaces:
            # List Deployments in the current namespace
            deployment_list = deployment_api.list_namespaced_deployment(namespace_name)

            annotation_added = False

            for deployment in deployment_list.items:
                deployment_name = deployment.metadata.name
                deployment_namespace = deployment.metadata.namespace

                # Get the current Deployment
                current_deployment = deployment_api.read_namespaced_deployment(deployment_name, deployment_namespace)

                # Check if metadata exists, or create it if it doesn't
                if not current_deployment.spec.template.metadata:
                    current_deployment.spec.template.metadata = client.V1ObjectMeta()

                # Check if annotations exist, or create it if it doesn't
                if not current_deployment.spec.template.metadata.annotations:
                    current_deployment.spec.template.metadata.annotations = {}

                # Add or update the annotation
                if annotation_key not in current_deployment.spec.template.metadata.annotations:
                    current_deployment.spec.template.metadata.annotations[annotation_key] = annotation_value
                    annotation_added = True

                # Apply the update
                deployment_api.patch_namespaced_deployment(deployment_name, deployment_namespace, current_deployment)

            if annotation_added:
                print(f"Annotation added to Deployments in Namespace: {namespace_name}")

            # Display the status of pods in the namespace
            print(f"Status of Pods in Namespace: {namespace_name}")
            pod_list = api_client.list_namespaced_pod(namespace_name)

            for pod in pod_list.items:
                print(f"Pod: {pod.metadata.name}")
                print(f"  Phase: {pod.status.phase}")
                print(f"  Conditions: {pod.status.conditions}")
                print("")

            print("=============================")
