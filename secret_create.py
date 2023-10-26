#pip install google-cloud-secret-manager; pip install kubernetes

import os
from google.cloud import secretmanager
from kubernetes import client, config

# Set the parameters for the script
project_id = "your-project-id"
secret_id = "your-secret-id"
namespace = "your-namespace"
k8s_secret_name = "your-k8s-secret-name"
secret_key_name = "your-secret-key-name"

# Authenticate using the Service Account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/app/service-account-key.json"
client = secretmanager.SecretManagerServiceClient()
name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

# Fetch the secret from Google Secret Manager
response = client.access_secret_version(request={"name": name})
secret_value = response.payload.data.decode("UTF-8")

# Initialize the Kubernetes client
config.load_incluster_config()
v1 = client.CoreV1Api()

# Create a Kubernetes Secret
body = client.V1Secret(
    data={secret_key_name: secret_value.encode("utf-8")},
    metadata=client.V1ObjectMeta(
        name=k8s_secret_name,
        namespace=namespace,
    ),
)

# Create the secret in the specified namespace
v1.create_namespaced_secret(namespace, body)
print(f"Kubernetes Secret '{k8s_secret_name}' created in namespace '{namespace}'")
