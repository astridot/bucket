Here’s a comprehensive documentation for your **Bucket Dependency Manager**, designed for easy understanding and practical use.

---

# Bucket Dependency Manager Documentation

### Author: **Astridot**  
### License: **Makoschin Free Software License (MFSL)**  

Bucket is a lightweight, flexible dependency manager designed for managing projects in any language. With features like branching, version control, and pull request management, it supports collaborative development and simplifies dependency handling.

---

## Features
- **Dependency Management**: Add, edit, list, install, and remove dependencies.
- **Branching**: Create, switch, list, and delete branches for isolated development workflows.
- **Versioning**: Save, list, and rollback to specific project states with version snapshots.
- **Pull Requests**: Create, list, view, and approve pull requests between branches.
- **Entrypoint Commands**: Set and run entrypoint commands for your project.

---

## Installation
Ensure you have Python 3.12 or later installed.

### Using `pip`:
```bash
pip install bkt
```

### CLI Commands
The CLI commands are invoked using `bucket` or `bucket<version>` (e.g. `bucket6`) after installation.

---

## Getting Started

### 1. Initialize a Bucket
To start using Bucket in a project:
```bash
bucket init
```
This creates a `.bucket` directory and sets up the necessary structure.

---

### 2. Manage Dependencies
 - **Add a dependency by specifying its name, source, and optional version or install command**:
  ```bash
  bucket dep add --name <name> --source <source> --version <version> --install-command <command>
  ```
- **List all dependencies**:
  ```bash
  bucket dep list
  ```
- **Remove a dependency**:
  ```bash
  bucket dep rm <name>
  ```
- **Install dependencies**:
  ```bash
  bucket dep install <name>
  ```

#### Example:
```bash
bucket dep add --name requests --source https://pypi.org/project/requests --version 2.31 --install-command "pip install requests==2.31"
```

---

### 3. Manage Branches
Branches allow isolated development for specific dependencies.

- **Create a branch**:
  ```bash
  bucket branch create --name <branch-name>
  ```
- **Switch to a branch**:
  ```bash
  bucket branch switch --name <branch-name>
  ```
- **List branches**:
  ```bash
  bucket branch list
  ```
- **Delete a branch**:
  ```bash
  bucket branch rm --name <branch-name>
  ```

---

### 4. Handle Pull Requests
Collaborate by merging changes using pull requests.

- **Create a pull request**:
  ```bash
  bucket pr create --source <source-branch> --target <target-branch> --description "<description>"
  ```
- **Approve and merge a pull request**:
  ```bash
  bucket pr approve --id1 <pr-id> --id2 <pr-id2>
  ```
- **List open pull requests**:
  ```bash
  bucket pr list
  ```
- **View a pull request**:
  ```bash
  bucket pr info --id1 <pr-id> --id2 <pr-id2>
  ```

---

### 5. Version Control
Track changes with snapshots of your project's state.

- **Save a version**:
  ```bash
  bucket vs commit
  ```
- **List saved versions**:
  ```bash
  bucket vs history
  ```
- **Rollback to a version**:
  ```bash
  bucket vs rollback --id1 <commit-id> --id2 <commit-id2>
  ```

---

### 6. Clean Up
Destroy the `.bucket` setup if no longer needed:
```bash
bucket destroy
```

---

## Example Workflow

1. Initialize a new project:
   ```bash
   bucket init
   ```
2. Create and switch to a feature branch:
   ```bash
   bucket branch create flask-dependency
   bucket branch switch flask-dependency
   ```
3. Add Flask dependency:
   ```bash
   bucket dep add --name flask --source https://pypi.org/project/flask --version 2.2.3 --install-command "pip install flask==2.2.3"
   ```
4. Commit the addition:
   ```bash
   bucket vs commit
   ```
5. Create a pull request to merge changes:
   ```bash
   bucket pr create --source flask-dependency --target main --description "Add Flask dependency to project."
   ```
6. Approve and merge the pull request:
   ```bash
   bucket pr approve 20242311 170224
   ```

---

## Additional Help
Run the following for detailed command help:
```bash
bucket --help
```

---

## Contributing
Feedback and contributions are welcome! Open issues or submit pull requests on the [GitHub repository](https://github.com/astridot/bucket).

---

## License
This project is licensed under the Makoschin Free Software License (MFSL) Version 2.0. See the source code headers for more details.