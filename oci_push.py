import os
import subprocess
import shutil
import urllib.request
import platform

def download_crane():
    version_url = "https://api.github.com/repos/google/go-containerregistry/releases/latest"
    version = subprocess.check_output(["curl", "-s", version_url]).decode("utf-8")
    version = version.split('"tag_name": "')[1].split('"')[0]

    os_name = platform.system()
    arch = "x86_64"  # Adjust as needed for different architectures

    crane_url = f"https://github.com/google/go-containerregistry/releases/download/{version}/go-containerregistry_{os_name}_{arch}.tar.gz"
    crane_path = "/usr/local/bin/crane"  # Change this if needed

    # Download crane binary
    urllib.request.urlretrieve(crane_url, "go-containerregistry.tar.gz")
    subprocess.run(["tar", "-zxvf", "go-containerregistry.tar.gz", "-C", "/usr/local/bin/", "crane"])
    
    # Make it executable
    os.chmod(crane_path, 0o755)

def tar_files(folder_path, tar_file):
    # Change to the specified folder
    os.chdir(folder_path)

    # Create a tar file
    tar_command = f"tar -cf {tar_file} *"
    subprocess.run(tar_command, shell=True)

def push_to_oci(tar_file, target_image):
    # Use crane to push the tar file to OCI
    crane_command = f"crane append -f {tar_file} -t {target_image}"
    subprocess.run(crane_command, shell=True)

if __name__ == "__main__":
    # Ensure crane is available or download it
    if shutil.which("crane") is None:
        download_crane()

    # Replace these values with your actual paths and image details
    manifests_folder = "/path/to/manifests"
    tar_filename = "file_name.tar"
    target_image = "europe-west2.docker.pkg.dev/project_name/rosync/cso:v1"

    # Step 1: Tar the files
    tar_files(manifests_folder, tar_filename)

    # Step 2: Push to OCI using crane
    push_to_oci(tar_filename, target_image)
