import os
import subprocess

def create_project_structure(base_path):
    directories = [
        "UE_Simulator",
        "Core_Network_Simulator",
        "Tests"
    ]

    for directory in directories:
        path = os.path.join(base_path, directory)
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {path}")

def create_readme(base_path):
    readme_path = os.path.join(base_path, "README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write("# 5G RAN Test Project\n")
        readme_file.write("This project contains scripts to test 5G RAN using UE simulator and Core Network simulator.\n")
    print(f"Created file: {readme_path}")

def main():
    base_path = os.path.abspath("5G_RAN_Test_Project")
    os.makedirs(base_path, exist_ok=True)
    print(f"Created project directory: {base_path}")

    create_project_structure(base_path)
    create_readme(base_path)

    # Initialize a new Python project with a virtual environment
    subprocess.run(["python", "-m", "venv", os.path.join(base_path, "venv")])
    print("Initialized virtual environment.")

if __name__ == "__main__":
    main()