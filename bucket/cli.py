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

try:
    import typer
    from .core import Bucket
    from typing import List, Optional

    app = typer.Typer()
    @app.command()
    def init():
        """Initialize a new Bucket"""
        bucket = Bucket()
        bucket.init()

    @app.command()
    def destroy():
        """Destroy an existing Bucket"""
        bucket = Bucket()
        bucket.destroy()

    @app.command()
    def run(args: List[str]):
        """Run the Bucket entrypoint command"""
        bucket = Bucket()
        bucket.run(args)

    @app.command()
    def set_property(property_: str, value: List[str]):
        """Set Bucket properties"""
        bucket = Bucket()
        bucket.set_property(property_, " ".join(value))

    @app.command()
    def dep(subcommand: str = typer.Argument(..., help="Subcommand", metavar="<add|edit|list|install|rm>"), name: Optional[str] = None, source: Optional[str] = None,
            version: Optional[str] = "latest", install_command: Optional[str] = None):
        """Manage Bucket dependencies"""
        bucket = Bucket()
        if subcommand == "add" or subcommand == "edit":
            bucket.add_or_edit_dependency(name, source, version, install_command, edit=subcommand=="edit")
        elif subcommand == "list":
            bucket.list_dependencies()
        elif subcommand == "install":
            bucket.install_dependencies(name or "*")
        elif subcommand == "rm":
            bucket.remove_dependency(name)

    @app.command()
    def vs(subcommand: str = typer.Argument(..., help="Subcommand", metavar="<commit|rollback|history>"), timestamp: Optional[str] = None, timestamp2: Optional[str] = None):
        """Manage Bucket versions"""
        bucket = Bucket()
        if subcommand == "commit":
            bucket.commit_version()
        elif subcommand == "rollback" and timestamp and timestamp2:
            bucket.rollback_version(f"{timestamp} {timestamp2}")
        elif subcommand == "history":
            bucket.list_versions()

    @app.command()
    def pr(subcommand: str = typer.Argument(..., help="Subcommand", metavar="<create|approve|list|info>"), source: Optional[str] = None, target: Optional[str] = None,
           description: Optional[str] = None, id1: Optional[str] = None, id2: Optional[str] = None):
        """Manage pull requests"""
        bucket = Bucket()
        if subcommand == "create" and source and target and description:
            bucket.create_pull_request(source, target, description)
        elif subcommand == "approve" and id1 and id2:
            bucket.approve_pull_request(f"{id1} {id2}")
        elif subcommand == "list":
            bucket.list_pull_requests()
        elif subcommand == "info" and id1 and id2:
            bucket.get_pull_request_description(f"{id1} {id2}")

    @app.command()
    def branch(subcommand: str = typer.Argument(..., help="Subcommand", metavar="<create|switch|rm|list>"), name: Optional[str] = None):
        """Manage branches"""
        bucket = Bucket()
        if subcommand == "create" and name:
            bucket.create_branch(name)
        elif subcommand == "switch" and name:
            bucket.switch_branch(name)
        elif subcommand == "rm" and name:
            bucket.delete_branch(name)
        elif subcommand == "list":
            bucket.list_branches()

    @app.command()
    def feedback():
        import os
        os.system("pwsh -Command start https://github.com/astridot/issues/new")

    if __name__ == "__main__":
        app()
except Exception as error: # NOQA
    import typer
    from tkinter.messagebox import showerror
    showerror(f"Bucket [{error.__class__.__name__}]", f"{error}\nUse `bucket feedback` to report this to the devs.")
    typer.echo(typer.style(f"Exited with {error.__class__.__name__}", fg=typer.colors.RED, bold=True))
    exit(1)