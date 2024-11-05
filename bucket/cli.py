import argparse
import os
import webbrowser

from .core import Bucket

def main():
    parser = argparse.ArgumentParser(description="Bucket")
    parser.add_argument('command', help="Bucket command to execute")
    parser.add_argument('subcommand', nargs='?', help="Subcommand for the primary command")
    parser.add_argument('args', nargs=argparse.REMAINDER, help="Arguments for the subcommand")
    parser.add_argument('-d', '--dir', default='.', help="Specify the directory for bucket operations")

    args = parser.parse_args()

    bucket = Bucket(directory=args.dir)

    if args.command == 'init':
        bucket.init()
    elif args.command == 'set':
        if args.subcommand == 'entrypoint' and len(args.args) >= 1:
            bucket.setEntrypoint(*args.args)
        elif args.subcommand == 'author' and len(args.args) >= 1:
            author = " ".join(args.args)
            bucket.setAuthor(author)
            print(f"Hello there, {author}!")
        else:
            print("Invalid or non-existent 'set' subcommand (or too few positional parameters filled). Use 'entrypoint' or 'author'.")
    elif args.command == 'run':
        bucket.run(args.args[1:])
    elif args.command == 'dep':
        if args.subcommand == 'add' and len(args.args) >= 2:
            name = args.args[0]
            source = args.args[1]
            version = args.args[2] if len(args.args) > 2 else "latest"
            install_command = args.args[3] if len(args.args) > 3 else None
            install_command = None if install_command == "_" else install_command
            bucket.add_dependency(name, source, version, install_command)
        elif args.subcommand == 'edit' and len(args.args) >= 2:
            name = args.args[0]
            source = args.args[1]
            version = args.args[2] if len(args.args) > 2 else "latest"
            install_command = " ".join(args.args[3:]) if len(args.args) > 3 else None
            install_command = None if install_command == "_"  else install_command
            bucket.edit_dependency(name, source, version, install_command)
        elif args.subcommand == 'list':
            bucket.list_dependencies()
        elif args.subcommand == 'install':
            dep_name = args.args[0] if args.args else '*'
            if dep_name == '*':
                bucket.install_all_dependencies()
            else:
                bucket.install_dependency(dep_name)
        elif args.subcommand == 'rm':
            dep_name = args.args[0] if args.args else None
            if dep_name:
                bucket.remove_dependency(dep_name)
            else:
                print("Specify a dependency name to remove or '*' to remove all.")
        else:
            print("Invalid or non-existent 'dep' subcommand (or too few positional parameters filled). Use 'add', 'list', 'install', or 'rm'.")
    elif args.command == 'ws':
        if args.subcommand == 'add' and len(args.args) >= 2:
            bucket.ws_add(args.args)
        elif args.subcommand == 'rm' and len(args.args) >= 2:
            bucket.ws_remove(args.args)
        elif args.subcommand in ('list', 'info'):
            bucket.ws_list()
        else:
            print("Invalid or non-existent 'ws' subcommand (or too few positional parameters filled). Use 'add', 'rm'.")
    elif args.command == 'web':
        if args.subcommand == 'update':
            if os.path.exists("info.html"):
                with open("info.html") as f:
                    bucket.updateInfo(f.read())
            else:
                print("No 'info.html' file found.")
        elif args.subcommand == 'open':
            webbrowser.open(f".bucket/index.html")
        else:
            print("Invalid or non-existent 'web' subcommand (or too few positional parameters filled). Use 'update' or 'open'.")
    else:
        print("Invalid or non-existent Bucket command. Use 'init', 'dep', 'run', 'web', 'set' or 'ws'.")