import subprocess
import sys

# Function to run a Python script
def run_script(script_name):
    try:
        subprocess.check_call([sys.executable, script_name])
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # First install dependencies
    run_script('install_dependencies.py')

    # Then run calcmain_opt.py
    run_script('calcmain_opt.py')
