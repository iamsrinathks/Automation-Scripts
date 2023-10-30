import subprocess

def list_resources_excluding_namespaces(excluded_namespaces):
  """Lists all the resources in the cluster excluding the specified namespaces.

  Args:
    excluded_namespaces: A list of namespace names to exclude.

  Returns:
    A list of all the resources in the cluster, excluding the specified namespaces.
  """

  # Get a list of all the resources in the cluster.
  all_resources = subprocess.check_output(["kubectl", "get", "all", "-A"], text=True).splitlines()

  # Exclude the specified namespaces.
  filtered_resources = []
  for resource in all_resources:
    if not resource.startswith(excluded_namespaces):
      filtered_resources.append(resource)

  return filtered_resources

# Example usage:

excluded_namespaces = ["kube-system", "default"]
filtered_resources = list_resources_excluding_namespaces(excluded_namespaces)

# Print the filtered list of resources.
for resource in filtered_resources:
  print(resource)









from kubernetes import client, config

# Set the namespaces you want to exclude from the rolling restart
excluded_namespaces = ["kube-system", "namespace-to-exclude"]  # Add namespaces to exclude here

def perform_rolling_restart(api_instance, namespace):
    # List resources in the specified namespace
    # You can adapt the following code to trigger a rolling restart for resources in the namespace.

def main():
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API client
    api_instance = client.CustomObjectsApi()
    v1 = client.CoreV1Api()

    # List all namespaces
    namespaces = v1.list_namespace().items

    # Perform a rolling restart for each namespace that is not excluded
    for namespace in namespaces:
        if namespace.metadata.name not in excluded_namespaces:
            print(f"Performing rolling restart in namespace: {namespace.metadata.name}")
            perform_rolling_restart(api_instance, namespace.metadata.name)
        else:
            print(f"Skipping namespace: {namespace.metadata.name}")

if __name__ == "__main__":
    main()
