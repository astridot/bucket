import os, json, subprocess, shutil, webbrowser


class Bucket:
    def __init__(self, directory="."):
        self.directory = directory
        self.name = os.path.basename(os.path.abspath(directory))
        self.bucket_dir = os.path.join(directory, ".bucket")
        self.meta_file = os.path.join(self.bucket_dir, "meta.json")
        self.dep_file = os.path.join(self.bucket_dir, "dependencies.json")
        self.html_file = os.path.join(self.bucket_dir, "index.html")
        self.author = os.getlogin()
        self.description = "No information available."

    def ensure_initialized(self, should_exist=True):
        exists = os.path.exists(self.bucket_dir)
        if should_exist != exists:
            msg = "Bucket not initialized. Run 'bucket init' first." if should_exist else \
                  "Bucket already initialized."
            print(msg)
            exit(1)

    @staticmethod
    def _load_json(file_path, default):
        return json.load(open(file_path)) if os.path.exists(file_path) else default

    @staticmethod
    def _save_json(file_path, data):
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4) # NOQA

    def init(self):
        self.ensure_initialized(should_exist=False)
        os.makedirs(self.bucket_dir, exist_ok=True)
        meta_data = {"name": self.name, "entrypoint": "", "author": self.author}
        self._save_json(self.meta_file, meta_data)
        self._save_json(self.dep_file, {})
        self.update_info(self.description)
        print(f"Bucket '{self.name}' initialized.")

    def destroy(self):
        self.ensure_initialized()
        shutil.rmtree(self.bucket_dir)
        print(f"Bucket '{self.name}' destroyed.")

    def set_property(self, key, value):
        self.ensure_initialized()
        meta_data = self._load_json(self.meta_file, {})
        meta_data[key] = value
        self._save_json(self.meta_file, meta_data)
        print(f"Set {key} to '{value}'.")

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
                print(f"No install command for {dep_name}, visit {details['source']} to install manually.")

    def update_info(self, content):
        self.description = content
        html_content = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<title>{self.name}</title>
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
        <h1 class="__title">{self.name}</h1>
        <h2 class="__subtitle">by {self.author}</h2>
    </div>
    <h3 class="__hint"><i>Scroll down to learn more about {self.name}</i></h3>
    <br>
</div>
<div class="body">
    <h2 class="__info_title"><u>Info</u></h2>
    <p class="__rights"><b>All rights over {self.name} belong to {self.author}.</b></p>
</div>
<p>{self.description}</p>
</body>
</html>"""
        with open(self.html_file, "w") as f:
            f.write(html_content)
        print("Updated info.")

    def manage_web(self, subcommand, arg):
        if subcommand == "update":
            self.update_info(arg)
        elif subcommand == "open":
            webbrowser.open(f"file://{os.path.abspath(self.html_file)}")