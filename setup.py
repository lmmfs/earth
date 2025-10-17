import subprocess
import sys

# Define file paths relative to the project root
DEV_REQS = 'api/requirements.txt'
TEST_REQS = 'requirements-dev.txt'

def run_command(command):
    """
    Executes a shell command and prints the output.
    """
    print(f"\n--- Executing: {' '.join(command)} ---")
    try:
        subprocess.check_call(command)
        print("--- Command successful ---")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)

def install_dependencies():
    """
    Installs dependencies to develop and test the software.
    """
    print("--- Installing Developing Dependencies ---")
    run_command([sys.executable, '-m', 'pip', 'install', '-r', DEV_REQS])

    print("--- Installing Testing Dependencies ---")
    run_command([sys.executable, '-m', 'pip', 'install', '-r', TEST_REQS])
    
    print("\n✅ All dependencies installed successfully.")


if __name__ == '__main__':
    install_dependencies()