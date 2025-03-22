import subprocess
import sys

# Function to install dependencies from requirements.txt
def install_from_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All dependencies are successfully installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing dependencies: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_from_requirements()