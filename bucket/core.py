"""
Bucket Dependency Manager by Astridot as part of Makoschin Free Software Distributions

This program is free software: you can redistribute it and/or modify
it under the terms of the Makoschin Free Software License (MFSL),
either version 1.0 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Makoschin Free Software License for more details.
"""

import os, json, subprocess, shutil, datetime

MAIN_BRANCH: str = "main"

class Bucket:
    def __init__(self, directory="."):
        self.directory = directory
        self.current_branch = MAIN_BRANCH  # Default branch is 'main'
        self.main_meta_file = os.path.join(".bucket", "branches", "main", "meta.json")
        if os.path.exists(self.main_meta_file): self.current_branch = self._load_json(self.main_meta_file, {})["current-branch"]
        self.name = os.path.basename(os.path.abspath(directory))
        self.bucket_dir = os.path.join(directory, ".bucket")
        self.branches_dir = os.path.join(self.bucket_dir, "branches")  # Directory for branches
        self.pr_dir = os.path.join(self.bucket_dir, "pull_requests")   # Directory for pull requests
        self.meta_file = os.path.join(self.branches_dir, self.current_branch, "meta.json")
        self.dep_file = os.path.join(self.branches_dir, self.current_branch, "dependencies.json")
        self.html_file = os.path.join(self.bucket_dir, "index.html")
        self.versions_dir = os.path.join(self.bucket_dir, "versions")
        self.author = os.getlogin()

    def ensure_initialized(self, should_exist=True):
        exists = os.path.exists(self.bucket_dir)
        if should_exist != exists:
            msg = "Bucket not initialized. Run 'bucket init' first." if should_exist else \
                  "Bucket already initialized."
            print(msg)
            exit(1)

    def _load_json(self, file_path, default): # NOQA
        if os.path.exists(file_path):
            return json.load(open(file_path))
        else:
            print(f"Error: {file_path} does not exist and cannot be loaded - Returning default value.")
            # uncomment this line ^ to check for bugs.
            return default

    def _save_json(self, file_path, data): # NOQA
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4) # NOQA

    def commit_version(self):
        """Save a version snapshot of meta and dependency files with timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d %H%M%S")
        version_path = os.path.join(self.versions_dir, timestamp)
        os.makedirs(version_path, exist_ok=True)
        shutil.copy(self.meta_file, os.path.join(version_path, "meta.json"))
        shutil.copy(self.dep_file, os.path.join(version_path, "dependencies.json"))
        print(f"Committed version at {timestamp}.")

    def rollback_version(self, timestamp):
        """Revert to a specific version based on timestamp."""
        version_path = os.path.join(self.versions_dir, timestamp)
        if os.path.exists(version_path):
            shutil.copy(os.path.join(version_path, "meta.json"), self.meta_file)
            shutil.copy(os.path.join(version_path, "dependencies.json"), self.dep_file)
            print(f"Rolled back to version {timestamp}.")
        else:
            print(f"Version {timestamp} not found.")

    def list_versions(self):
        """List all saved versions with timestamps."""
        if os.path.exists(self.versions_dir):
            versions = os.listdir(self.versions_dir)
            print("Available versions:")
            for v in sorted(versions):
                print(f" - {v}")
        else:
            print("No versions found.")

    def init(self):
        self.ensure_initialized(should_exist=False)
        os.makedirs(os.path.join(self.branches_dir, MAIN_BRANCH), exist_ok=True)
        os.makedirs(self.bucket_dir, exist_ok=True)
        os.makedirs(self.branches_dir, exist_ok=True)
        os.makedirs(self.pr_dir, exist_ok=True)
        meta_data = {
            "name": self.name,
            "entrypoint": "",
            "author": self.author,
            "current-branch": MAIN_BRANCH
        }
        print(f"Bucket '{self.name}' initialized successfully on branch 'main'.")
        self._save_json(self.meta_file, meta_data)
        self._save_json(self.dep_file, {})
        self.commit_version()

    def create_branch(self, branch_name, init=False):
        """Create a new branch based on the current state."""
        branch_path = os.path.join(self.branches_dir, branch_name)
        if not os.path.exists(branch_path):
            os.makedirs(branch_path)
            shutil.copy(self.meta_file, os.path.join(branch_path, "meta.json"))
            shutil.copy(self.dep_file, os.path.join(branch_path, "dependencies.json"))
            print(f"Branch '{branch_name}' created.")
        elif init:
            print(f"Branch '{branch_name}' already exists.")

    def switch_branch(self, branch_name):
        """Switch to an existing branch by replacing current files."""
        branch_path = os.path.join(self.branches_dir, branch_name)
        if os.path.exists(branch_path):
            self.current_branch = branch_name
            self._save_json(self.main_meta_file, self._load_json(self.main_meta_file, {"current-branch": MAIN_BRANCH}) | {"current-branch": branch_name})
            print(f"Switched to branch '{branch_name}'.")
        else:
            print(f"Branch '{branch_name}' does not exist.")

    def list_branches(self):
        """Lists all available branches in the branches directory."""
        self.ensure_initialized()
        current_branch = self._load_json(self.meta_file, {"current-branch": MAIN_BRANCH})["current-branch"]
        if not os.path.exists(self.branches_dir):
            print("No branches found.")
            return

        branches = [name for name in os.listdir(self.branches_dir) if
                    os.path.isdir(os.path.join(self.branches_dir, name))]
        if not branches:
            print("No branches found.")
        else:
            print("Available branches:")
            for branch in branches:
                print(f" - {branch}{" (current)" if branch == current_branch else ""}")

    def delete_branch(self, branch_name):
        """Deletes a specified branch from the branch directory."""
        self.ensure_initialized()
        branch_path = os.path.join(self.branches_dir, branch_name)
        current_branch = self._load_json(self.meta_file, {"current-branch": MAIN_BRANCH})["current-branch"]

        if branch_name == MAIN_BRANCH:
            print(f"Cannot delete {MAIN_BRANCH} branch.")
        elif branch_name == current_branch:
            print(f"Cannot delete current branch.")
        elif not os.path.exists(branch_path):
            print(f"Branch '{branch_name}' does not exist.")
        else:
            shutil.rmtree(branch_path)
            print(f"Branch '{branch_name}' deleted successfully.")

    def create_pull_request(self, source_branch, target_branch, description):
        """Create a pull request from source_branch to target_branch."""
        pr_id = datetime.datetime.now().strftime("%Y%m%d %H%M%S")
        pr_path = os.path.join(self.pr_dir, pr_id)
        os.makedirs(pr_path)
        pr_data = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "description": description,
            "status": "open"
        }
        self._save_json(os.path.join(pr_path, "pr.json"), pr_data)
        print(f"Pull request '{pr_id}' created from '{source_branch}' to '{target_branch}'.")

    def list_pull_requests(self):
        """List all open pull requests."""
        prs = os.listdir(self.pr_dir)
        print("Open pull requests:")
        for pr_id in prs:
            pr_data = self._load_json(os.path.join(self.pr_dir, pr_id, "pr.json"), {})
            if pr_data.get("status") == "open":
                print(f"{pr_id}: {pr_data['source_branch']} -> {pr_data['target_branch']} | [{pr_data['description']}]")

    def get_pull_request_description(self, pr_id):
        """Get the description of a pull request."""
        path = os.path.join(self.pr_dir, pr_id, "pr.json")
        if os.path.exists(path):
            pr_data = self._load_json(path, {})
            print(f"Description: '{pr_data["description"]}'")
            print(f"PR ID: '{pr_id}'")
            print(f"Source branch: '{pr_data["source_branch"]}'")
            print(f"Target branch: '{pr_data["target_branch"]}'")
            print(f"Status: {pr_data["status"].upper()}")
        else:
            print(f"Branch '{pr_id}' does not exist.")

    def approve_pull_request(self, pr_id):
        """Merge changes from the source branch to the target branch for the specified PR."""
        pr_data = self._load_json(os.path.join(self.pr_dir, pr_id, "pr.json"), {})
        if pr_data and pr_data["status"] == "open":
            source_branch = pr_data["source_branch"]
            target_branch = pr_data["target_branch"]

            # Load source branch files and overwrite target branch files
            source_path = os.path.join(self.branches_dir, source_branch)
            target_path = os.path.join(self.branches_dir, target_branch)
            if os.path.exists(source_path) and os.path.exists(target_path):
                shutil.copy(os.path.join(source_path, "meta.json"),
                            os.path.join(target_path, "meta.json"))
                shutil.copy(os.path.join(source_path, "dependencies.json"),
                            os.path.join(target_path, "dependencies.json"))
                pr_data["status"] = "merged"
                self._save_json(os.path.join(self.pr_dir, pr_id, "pr.json"), pr_data)
                print(f"Pull request '{pr_id}' approved and merged into '{target_branch}'.")
            else:
                print(f"Error: Branch '{source_branch}' or '{target_branch}' does not exist.")
        else:
            print(f"Pull request '{pr_id}' not found or already merged.")

    def set_property(self, key, value):
        self.ensure_initialized()
        meta_data = self._load_json(self.meta_file, {})
        meta_data[key] = value
        self._save_json(self.meta_file, meta_data)
        self.commit_version()  # Save version after property change
        print(f"Set {key} to '{value}'.")

    def destroy(self):
        self.ensure_initialized()
        shutil.rmtree(self.bucket_dir)
        print(f"Bucket '{self.name}' destroyed.")

    def run(self, args=None):
        self.ensure_initialized()
        meta_data = self._load_json(self.meta_file, {})
        entrypoint = meta_data.get("entrypoint")
        if entrypoint:
            subprocess.run(f"{entrypoint} {' '.join(args or [])}", shell=True)
        else:
            print("No entrypoint set. Use 'bucket set entrypoint <command>'.")

    def add_or_edit_dependency(self, name, source, version="latest", install_command=None, edit=False):
        self.ensure_initialized()
        dependencies = self._load_json(self.dep_file, {})
        dependencies[name] = {"source": source, "version": version, "install_command": install_command}
        self._save_json(self.dep_file, dependencies)
        action = "Edited" if edit else "Added"
        print(f"{action} dependency '{name}'.")

    def list_dependencies(self):
        self.ensure_initialized()
        dependencies = self._load_json(self.dep_file, {})
        if dependencies:
            for name, details in dependencies.items():
                print(f"{name}: {details['source']} (version: {details['version']})")
        else:
            print("No dependencies found.")

    def remove_dependency(self, name):
        self.ensure_initialized()
        dependencies = self._load_json(self.dep_file, {})
        if name == "*":
            dependencies.clear()
            print("All dependencies removed.")
        elif name in dependencies:
            del dependencies[name]
            print(f"Removed dependency '{name}'.")
        else:
            print(f"Dependency '{name}' not found.")
        self._save_json(self.dep_file, dependencies)

    def install_dependencies(self, name="*"):
        self.ensure_initialized()
        dependencies = self._load_json(self.dep_file, {})
        to_install = dependencies if name == "*" else {name: dependencies.get(name)}
        for dep_name, details in to_install.items():
            install_command = details.get("install_command")
            if install_command:
                print(f"Installing {dep_name}...")
                subprocess.run(install_command, shell=True)
            else:
                if details["source"].startswith("http"):
                    os.system(f"pwsh -Command start {details["source"]}")
                else:
                    os.system(f"pwsh -Command start \"'https://google.com/search?q={dep_name} {details["version"]} {details["source"]} install'\"")