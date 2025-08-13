import os
import sys
import subprocess
import pkg_resources

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

def parse_requirements(file_path):
    """
    Parse requirements.txt file and return a list of requirements.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    requirements = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            requirements.append(line)
    
    return requirements

def check_package_installed(requirement):
    """
    Check if a specific package with version requirement is installed.
    """
    try:
        pkg_resources.require(requirement)
        return True
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
        return False

def package_checker():
    """
    Check if necessary Python packages are installed.
    """
    missing_packages = []
    requirements = parse_requirements('requirements.txt')

    for requirement in requirements:
        if not check_package_installed(requirement):
            missing_packages.append(requirement)

    # Print the result
    if missing_packages:
        print("The following packages are missing or have version conflicts:")
        for pkg in missing_packages:
            print(f" - {pkg}")
        print("\nAttempting to install missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("Missing packages installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install missing packages: {e}")
    else:
        print("All packages are installed successfully.")


if __name__ == "__main__":
    print("Testing package installation...")
    package_checker()
    print("Package installation test passed")