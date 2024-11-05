import os
import json
import subprocess
import webbrowser
import shutil


HTML_CONTENT: str = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<title>{name}</title>
<style>
    body {{
        font-family: Arial, sans-serif;
    }}
    .header {{
        background-image: linear-gradient(to bottom right, #00a6ff, #0055ff);
        color: white;
        padding: 20px;
        text-align: center;
    }}
    .title-container {{
        display: flex;
        align-items: baseline;
        justify-content: center;
        gap: 20px;
    }}
    .__title {{
        font-size: 10em;
        margin: 0;
    }}
    .__subtitle {{
        font-size: 3em;
        margin: 0;
    }}
    .__info_title {{
        font-size: 4.5em;
    }}
    .__rights {{
        font-size: 2em;
    }}
    .body {{
        color: black;
        padding: 20px;
    }}
</style>
</head>
<body>
<div class="header">
    <br>
    <div class="title-container">
        <h1 class="__title">{name}</h1>
        <h2 class="__subtitle">by {author}</h2>
    </div>
    <h3 class="__hint"><i>Scroll down to learn more about {name}</i></h3>
    <br>
</div>
<div class="body">
    <h2 class="__info_title"><u>Info</u></h2>
    <p class="__rights"><b>All rights over {name} belong to {author}.</b></p>
</div>
<p>{desc}</p>
</body>
</html>
""" # you can collapse this, and it looks much better :)

class Bucket:
    def __init__(self, directory='.'):
        self.directory = directory
        self.name: str = os.path.basename(os.path.abspath(self.directory))
        self.bucket_dir = os.path.join(directory, '.bucket')
        self.meta_file = os.path.join(self.bucket_dir, 'meta.json')
        self.dep_file = os.path.join(self.bucket_dir, 'dependencies.json')
        self.html_file = os.path.join(self.bucket_dir, 'index.html')
        self.author = "AnonymousCreator"
        self.description = "No info provided :("
        if os.path.exists("../README.md"):
            with open("../README.md") as f:
                self.description = f.read()
    def ensure(self):
        if not os.path.exists(self.bucket_dir):
            print("Bucket not initialized. Run 'bucket init' first.")
            exit(1)
    def init(self):
        """Initialize the .bucket directory and configuration files."""
        os.makedirs(self.bucket_dir, exist_ok=True)
        meta_data = {
            "name": self.name,
            "entrypoint": "",
            "author": self.author
        }
        if not os.path.exists(self.meta_file):
            with open(self.meta_file, 'w') as f:
                json.dump(meta_data, f, indent=4)
            print(f"Initialized {self.meta_file}")
        if not os.path.exists(self.dep_file):
            with open(self.dep_file, 'w') as f:
                json.dump({}, f, indent=4)
            print(f"Initialized {self.dep_file}")
        self.updateInfo("No info provided :(")
    def updateInfo(self, content: str) -> None:
        self.description = content
        with open(self.meta_file, 'r') as f:
            meta_data = json.load(f)
            self.author = meta_data.get('author')
        with open(self.html_file, 'w') as f:
            f.write(HTML_CONTENT.format(
                name=self.name,
                desc=self.description,
                author=self.author
            ))
        print(f"Updated info successfully.")
    def setEntrypoint(self, *args):
        """Set the entrypoint command for the bucket."""
        self.ensure()
        command = ' '.join(args)
        if os.path.exists(self.meta_file):
            with open(self.meta_file, 'r+') as f:
                meta_data = json.load(f)
                meta_data['entrypoint'] = command
                f.seek(0)
                json.dump(meta_data, f, indent=4)
                f.truncate()
            print(f"Entrypoint set to: {command}")
        else:
            print("Bucket not initialized. Run 'bucket init' first.")
    def setAuthor(self, author):
        """Set the entrypoint command for the bucket."""
        self.ensure()
        if os.path.exists(self.meta_file):
            with open(self.meta_file, 'r+') as f:
                meta_data = json.load(f)
                meta_data['author'] = author
                self.author = author
                f.seek(0)
                json.dump(meta_data, f, indent=4)
                f.truncate()
            print(f"Author set to {author}.")
        else:
            print("Bucket not initialized. Run 'bucket init' first.")
    def run(self, args: list[str] | None = None):
        """Run the entrypoint command."""
        self.ensure()
        args = args or []
        if os.path.exists(self.meta_file):
            with open(self.meta_file, 'r') as f:
                meta_data = json.load(f)
                entrypoint = meta_data.get('entrypoint')
                if entrypoint:
                    subprocess.run(f"{entrypoint} {" ".join(args)}", shell=True, cwd=self.directory)
                else:
                    print("No entrypoint set. Use 'bucket entrypoint set <command>'.")
        else:
            print("Bucket not initialized. Run 'bucket init' first.")

    def add_dependency(self, name, source, version="latest", install_command=None):
        self.ensure()
        """Add a dependency with optional version and install command."""
        if os.path.exists(self.dep_file):
            with open(self.dep_file, 'r+') as f:
                dependencies = json.load(f)
                if name in list(dependencies.keys()):
                    print(f"Dependency '{name}' already exists. (try e.g. '{name}2', '{name}-alt', '{name}-copy, etc.")
                    print(f"Looking to edit properties of '{name}'? Run 'bucket dep edit \"{name}\" \"{source}\" \"{version}\" \"{install_command or "_"}\"'")
                else:
                    dependencies[name] = {
                        "source": source,
                        "version": version,
                        "install-command": install_command
                    }
                    f.seek(0)
                    json.dump(dependencies, f, indent=4)
                    f.truncate()
                    print(f"Added dependency: {name} from {source} (version: {version})")
                    print(f"Use 'bucket dep remove {name}' to remove it,")
                    print("or 'bucket dep remove *' to remove all dependencies in this bucket.")
        else:
            print("Bucket not initialized. Run 'bucket init' first.")

    def edit_dependency(self, name, source, version="latest", install_command=None):
        """Add a dependency with optional version and install command."""
        self.ensure()
        if os.path.exists(self.dep_file):
            with open(self.dep_file, 'r+') as f:
                dependencies = json.load(f)
                if name not in list(dependencies.keys()):
                    print(f"Dependency '{name}' doesn't exist.")
                    print(f"Looking to create '{name}'? Run 'bucket dep add \"{name}\" \"{source}\" \"{version}\" \"{install_command or "_"}\"'")
                else:
                    dependencies[name] = {
                        "source": source,
                        "version": version,
                        "install-command": install_command
                    }
                    f.seek(0)
                    json.dump(dependencies, f, indent=4)
                    f.truncate()
                    print(f"Edited dependency: {name} from {source} (version: {version})")
        else:
            print("Bucket not initialized. Run 'bucket init' first.")

    def list_dependencies(self):
        """List all dependencies along with their details."""
        self.ensure()
        if os.path.exists(self.dep_file):
            with open(self.dep_file, 'r') as f:
                dependencies = json.load(f)
                if dependencies:
                    for name, details in dependencies.items():
                        print(f"{name}: {details['source']} (version: {details['version']}) [quick install using Bucket: 'bucket dep install {name}']")
                    print("[quick install all dependencies at once using Bucket: 'bucket dep install *']")
                else:
                    print("No dependencies added.")
        else:
            print("Bucket not initialized. Run 'bucket init' first.")

    def remove_dependency(self, name):
        """Remove a specific dependency by name or all dependencies if '*' is specified."""
        self.ensure()
        if os.path.exists(self.dep_file):
            with open(self.dep_file, 'r+') as f:
                dependencies = json.load(f)
                if name == '*':
                    print(f"Removed {", ".join([('\'' + d + '\'') for d in list(dependencies.keys())])}")
                    dependencies.clear()
                elif name in list(dependencies.keys()):
                    source = dependencies[name]["source"]
                    version = dependencies[name]["version"]
                    install_command = dependencies[name]["install-command"]
                    del dependencies[name]
                    print(f"Removed dependency: {name}")
                    print(f"Use 'bucket dep add \"{name}\" \"{source}\" \"{version}\" \"{install_command or "_"}\"' to undo this removal.")
                else:
                    print(f"Dependency '{name}' not found.")
                # Write the updated dependencies back to the file
                f.seek(0)
                json.dump(dependencies, f, indent=4)
                f.truncate()
        else:
            print("Bucket not initialized. Run 'bucket init' first.")

    def install_dependency(self, name):
        """Install a specific dependency by its name, using the installation command or Google search if missing."""
        self.ensure()
        if os.path.exists(self.dep_file):
            with open(self.dep_file, 'r') as f:
                dependencies = json.load(f)
                dependency = dependencies.get(name)
                if dependency:
                    install_command = dependency.get("install-command")
                    source = dependency["source"]
                    version = dependency["version"]

                    if install_command:
                        print(f"Installing {name} using command: {install_command}")
                        subprocess.run(install_command, shell=True, cwd=self.directory)
                    else:
                        query = f"{name} {source} download" if version == "latest" else f"{name} {version} {source} download"
                        url = f"https://google.com/search?q={query}"
                        print(f"No install command for {name}. Searching online: {url}")
                        webbrowser.open(url)
                else:
                    print(f"Dependency '{name}' not found.")
        else:
            print("Bucket not initialized. Run 'bucket init' first.")

    def install_all_dependencies(self):
        """Install all dependencies listed in dependencies.json."""
        self.ensure()
        if os.path.exists(self.dep_file):
            with open(self.dep_file, 'r') as f:
                dependencies = json.load(f)
                for name, details in dependencies.items():
                    install_command = details.get("install-command")
                    source = details["source"]
                    version = details["version"]

                    if install_command:
                        print(f"Installing {name} using command: {install_command}")
                        subprocess.run(install_command, shell=True, cwd=self.directory)
                    else:
                        query = f"{name} {source} download" if version == "latest" else f"{name} {version} {source} download"
                        url = f"https://google.com/search?q={query}" if not source.startswith("http") else f"{source}"
                        print(f"No install command for {name}. Searching online: {url}")
                        webbrowser.open(url)
        else:
            print("Bucket not initialized. Run 'bucket init' first.")
    def ws_list(self) -> None:
        self.ensure()
        print(f'Files and directories in: {os.getcwd()}')
        dirs: list[str] = os.listdir()
        is_bucket: bool = True
        try:
            dirs.remove(".bucket")
        except ValueError:
            is_bucket = False
        print(*dirs, sep='\n')
        print(f"BUCKET={str(is_bucket).lower()}")
    def ws_add(self, args) -> None:
        self.ensure()
        if args[0] == 'file':
            file: str = " ".join(args[1:])
            if not os.path.exists(file):
                with open(file, "w") as f:
                    f.write("")
                print(f"Added file '{file}'.")
                self.addToGit(file)
            else:
                print(f"File '{file}' already exists.")
        elif args[0] == 'dir':
            file: str = " ".join(args[1:])
            if not os.path.exists(file):
                os.mkdir(file)
                print(f"Added directory '{file}'.")
            else:
                print(f"Directory '{file}' already exists.")
            self.addToGit(file)
        else:
            print("Invalid or non-existent 'ws add' subcommand (or too few positional parameters filled). Use 'file' or 'dir'.")
    def ws_remove(self, args) -> None:
        self.ensure()
        if args[0] == 'file':
            file: str = " ".join(args[1:])
            if os.path.exists(file):
                os.remove(file)
                print(f"Removed file '{file}'.")
            else:
                print(f"File '{file}' doesn't exist.")
        elif args[0] == 'dir':
            file: str = " ".join(args[1:])
            if os.path.exists(file):
                shutil.rmtree(file)
                print(f"Removed directory '{file}'.")
            else:
                print(f"Directory '{file}' doesn't exist.")
        else:
            print("Invalid or non-existent 'ws rm' subcommand (or too few positional parameters filled). Use 'file' or 'dir'.")
    def addToGit(self, file: str) -> None:
        self.ensure()
        if os.path.exists(".git"):
            os.system(f"git add \"{file}\"")
            print(f"Bucket has added '{file}' to git automatically. You can use 'git rm \"{file}\"' to undo this.")