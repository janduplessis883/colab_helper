import subprocess
import sys
import os

is_colab = "google.colab" in sys.modules


def install_requirements():
    """Installs the required packages for the project."""

    requirements_file = "requirements.txt"

    # Check if requirements.txt exists
    if not os.path.exists(requirements_file):
        print("❌ Error: requirements.txt file not found.")
        return False

    print("⏳ Installing base requirements ...")

    cmd = ["python", "-m", "pip", "install", "-r", requirements_file]
    process_install = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    if process_install.returncode != 0:
        # If there was an error, print it and return False
        print("❌ Error installing packages:")
        print(process_install.stderr.decode())
        return False

    # If everything went well, print success and return True
    print("✅ Installation successful.")
    return True
