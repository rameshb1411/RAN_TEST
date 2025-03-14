import os
import subprocess

# Define the commit message
commit_message = "Add untracked files and update repository"


def run_command(command, env=None):
    """Run a command in the shell and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Command failed with error: {result.stderr}")
    return result.stdout


def main():
    # Define the environment variables
    env = os.environ.copy()
    env["PATH"] = "C:\\Users\\Ramesh1\\PycharmProjects\\PythonProject2\\.venv\\Scripts;" + env["PATH"]

    # Retrieve email, username, token, and repo from environment variables
    git_user_name = env.get('GITHUB_USERNAME')
    git_user_email = env.get('GITHUB_EMAIL')
    git_token = env.get('GITHUB_TOKEN')
    git_repo = env.get('GITHUB_REPO_RAN')

    if not git_user_name or not git_user_email or not git_token or not git_repo:
        print(
            "Error: One or more environment variables (GITHUB_USERNAME, GITHUB_EMAIL, GITHUB_TOKEN, GITHUB_REPO_RAN) are not set.")
        return

    # Ensure git_repo does not contain 'https://' and strip any leading/trailing whitespace
    git_repo = git_repo.replace('https://', '').strip()

    # Change to the repository directory
    repo_dir = "C:\\Users\\Ramesh1\\PycharmProjects\\PythonProject2\\RAN_TEST"
    os.chdir(repo_dir)

    # Check if the directory is a Git repository
    if not os.path.exists(os.path.join(repo_dir, ".git")):
        print("Directory is not a Git repository. Initializing a new Git repository.")
        run_command("git init", env=env)
        run_command(f"git remote add origin https://{git_user_name}:{git_token}@{git_repo}.git", env=env)

    # Update the remote URL to ensure it uses the correct format
    output = run_command(f"git remote set-url origin https://{git_user_name}:{git_token}@{git_repo}.git", env=env)
    if output:
        print(f"git remote set-url output: {output}")

    # Configure Git to use stored tokens and credentials
    print("Configuring Git to use stored tokens and credentials.")
    output = run_command(f"git config user.name '{git_user_name}'", env=env)
    if output:
        print(f"git config user.name output: {output}")

    output = run_command(f"git config user.email '{git_user_email}'", env=env)
    if output:
        print(f"git config user.email output: {output}")

    output = run_command("git config credential.helper store", env=env)
    if output:
        print(f"git config credential.helper output: {output}")

    # Add all untracked files to the staging area
    print("Adding all untracked files to the staging area.")
    output = run_command("git add .", env=env)
    if output:
        print(f"git add output: {output}")

    # Commit the changes
    output = run_command(f"git commit -m \"{commit_message}\"", env=env)
    if output:
        print(f"git commit output: {output}")

    # Push the changes to the remote repository
    output = run_command("git push -u origin master", env=env)
    if output:
        print(f"git push output: {output}")


if __name__ == "__main__":
    main()