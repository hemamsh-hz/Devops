# Task Management API — DevOps Assignment

**Course:** 25CIAEC59 / 25CYAEC59 · **Total:** 20 marks (Component 1: 10, Component 2: 10)  
**GitHub account:** `Bharath-190`  
**Suggested repository name:** `devops-task`  
**Repository URL:** `https://github.com/Bharath-190/devops-task`

This project follows the assignment's requested sequence and reuses one small REST API for both components. It uses Python/FastAPI, which the assignment permits, rather than Maven/Gradle. The CI pipeline builds a Python wheel and runs tests.

> **Important:** The GitHub repository, Jenkins CI pipeline, Ansible deployment, Docker image, and local Kubernetes deployment have been implemented and tested. Do not put screenshots of commands that have not actually succeeded into the final report.

## Assignment pipeline

`Code → Git/GitHub → Jenkins (test + wheel build) → Ansible (server configuration) → Docker image → Kubernetes (3 replicas → 5 replicas)`

## Application endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Health check used by Docker/Kubernetes probes |
| GET | `/todos` | List in-memory tasks |
| POST | `/todos` | Add a task: `{"title":"Finish assignment"}` |
| GET | `/todos/{task_id}` | Retrieve one task |

The task list is deliberately in memory; it resets when the process restarts. There is no database, as suggested in the assignment.

## 2. Before you start — setup checklist

Install Git, Python 3.10+ (3.12 recommended), pip/venv, Docker, Ansible on a Linux/WSL control machine, Jenkins, and Minikube or Kind. A public GitHub account is sufficient; paid cloud services are not required. On Windows, use WSL2 Ubuntu for Ansible and a supported Docker/Kubernetes setup. On EndeavourOS, install the equivalent packages with `pacman` and run Ansible from the Linux host.

Check tools:

```bash
git --version
python3 --version
python3 -m pip --version
docker --version
ansible --version
kubectl version --client
minikube version
```

Jenkins needs a Java runtime compatible with your selected Jenkins release, plus Python 3 and pip available to the agent. Install Jenkins from the official Jenkins instructions for your OS; this repository does not bundle or modify Jenkins itself.

## 3. Component 1 — CI pipeline with Git, Python and Jenkins (10 marks)

### Step 1: Create and test the application

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements-dev.txt
pytest
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

In a second terminal:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/todos
curl -X POST http://127.0.0.1:8000/todos -H 'Content-Type: application/json' -d '{"title":"Finish DevOps assignment"}'
curl http://127.0.0.1:8000/todos/1
```

Open interactive API documentation at `http://127.0.0.1:8000/docs`. Stop the server with Ctrl+C.

### Step 2: Set up Git and GitHub

Create a **new empty repository** named `devops-task` under `Bharath-190` (do not initialize it with a README, license, or `.gitignore`, because these files already exist in this bundle). Then, from this folder:

```bash
git init -b main
git config user.name "YOUR NAME"
git config user.email "YOUR_GITHUB_NOREPLY_OR_EMAIL"
git add .
git commit -m "Initial Task API and DevOps pipeline"
git remote add origin https://github.com/Bharath-190/devops-task.git
git push -u origin main

git switch -c feature/health-and-tests
# Make a small real change, e.g. improve a comment or add a meaningful test.
git add .
git commit -m "Add health check and regression tests"
git push -u origin feature/health-and-tests
```

Create a pull request from `feature/health-and-tests` into `main` on GitHub and merge it. If you work locally instead, `git switch main && git merge --no-ff feature/health-and-tests` is also acceptable according to the assignment. Confirm the history:

```bash
git branch -a
git log --oneline --graph --decorate --all
```

**Evidence:** screenshot the branches and merge in the history. If the branch is merged on GitHub, pull `main` locally afterwards.

### Step 3: Configure the build

The project uses `pyproject.toml` as its package/build configuration. Run:

```bash
python -m pip install -r requirements-dev.txt
python -m build --wheel
ls -l dist/
```

A `.whl` file should be created in `dist/`. It is the build artifact archived by the Jenkins pipeline. This Python build replaces the assignment's Maven/Gradle command because Python/FastAPI is an allowed language/framework choice.

### Step 4: Set up Jenkins (required CI evidence)

1. Ensure Jenkins can run `git`, `python3`, and `pip` on the executor/agent. The `sh` steps assume a Linux/WSL agent.
2. In Jenkins, choose **New Item → Pipeline** and name it `task-api-ci`.
3. Under **Pipeline**, choose **Pipeline script from SCM**, SCM **Git**, and enter `https://github.com/Bharath-190/devops-task.git`; choose branch `*/main`; script path `Jenkinsfile`.
4. Configure credentials if the repository is private. Do not store credentials or tokens in source files.
5. Save and run the first build once. The Jenkinsfile polls SCM every two minutes (`pollSCM('H/2 * * * *')`) so pushes are picked up automatically without requiring a public webhook endpoint.
6. Push a small source change and verify a new build is triggered automatically. The first manual run alone does not prove automatic CI.
7. Inspect **Console Output** and **Build Artifacts**. The artifact is versioned with Jenkins build number and short Git SHA.

If your Jenkins controller/agent runs only on Windows, configure a Linux agent or adapt `sh` steps to `bat`/PowerShell; do not assume the provided Jenkinsfile works unchanged on a Windows-only agent.

### Step 5: CI enhancement implemented

**Enhancement:** automated unit tests run before the wheel build. Jenkins runs five regression tests using pytest and publishes JUnit-format results. The wheel is also archived under `artifacts/task-api-<BUILD_NUMBER>-<SHORT_SHA>.whl`, tying the output to the source commit. `.github/workflows/ci.yml` provides a second CI implementation on pushes and pull requests.

**Evidence to capture (from the assignment):**
- Git branch/commit history including the merge.
- Jenkins job configuration showing SCM, trigger/polling and pipeline file.
- Successful Jenkins console output showing checkout, tests and build.
- Archived, versioned wheel artifact.
- Passing test results and/or successful GitHub Actions run.

## 4. Component 2 — Ansible + Docker + Kubernetes (10 marks)

Use the same repository and API.

### Step 1: Write and run the Ansible playbook

The playbook is at `ansible/playbook.yml`; the role is at `ansible/roles/task_api`. It installs Python runtime packages, creates a service account and application directory, copies the built Python wheel to the target host, creates a virtual environment, installs the wheel and its declared dependencies, installs a systemd service, and enables/starts it. The `app_port` variable is configurable. The `Restart task-api` handler restarts the service when source, dependencies, or unit configuration changes.

Run Ansible from Linux/WSL or another Linux control machine with Ansible installed. By default, `ansible/inventory.ini` targets `localhost`; use this only on a Linux host with systemd and become/sudo permissions. To target an Ubuntu VM, edit the inventory as described in the comments and make sure SSH and privilege escalation work.

```bash
cd ansible
ansible --version
ansible-playbook -i inventory.ini playbook.yml --ask-become-pass
curl http://127.0.0.1:8000/health
```

The last curl is appropriate when the playbook targeted the same host. For a VM, use the VM's reachable IP. If port 8000 is already used by another instance, stop that process first or change `app_port` in `playbook.yml`.

### Step 2: Containerize with Docker

Run from the project root:

```bash
docker build -t task-api:1.0.0 .
docker run --rm -d --name task-api -p 8000:8000 task-api:1.0.0
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/todos
docker logs task-api
docker stop task-api
```

The Dockerfile uses a builder stage to build wheels and a small Python runtime stage to run as a non-root user. The image also has a Docker health check.

### Step 3: Deploy on Kubernetes

Install/start **Minikube** or **Kind** first. For Minikube, build the image in Minikube's Docker daemon so the local cluster can see it:

```bash
minikube start
eval "$(minikube docker-env)"       # Linux/macOS shell; use PowerShell-specific syntax on Windows
docker build -t task-api:1.0.0 .
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get deployments
kubectl get pods -l app=task-api
kubectl get svc task-api-service
```

In a separate terminal, get a URL and call it:

```bash
minikube service task-api-service --url
# Use the URL printed by the previous command:
curl <URL_FROM_MINIKUBE>/health
```

For Kind instead, build the image with Docker and then run `kind load docker-image task-api:1.0.0`; apply both YAML files. If the image cannot be found, verify image name/tag and that it has been loaded into the cluster's runtime.

The Deployment starts with **3 replicas**. The Service selector matches the Deployment's `app: task-api` labels. The NodePort is 30080; on Minikube, prefer the URL printed by `minikube service`.

### Step 4: Demonstrate scaling

```bash
kubectl scale deployment/task-api --replicas=5
kubectl get pods -l app=task-api -w
# In another terminal, or after the pods settle:
kubectl get deployment task-api
kubectl scale deployment/task-api --replicas=3
kubectl get pods -l app=task-api
```

Take one screenshot showing 3 pods and another showing 5 pods running. Wait until pods are `Running`/`Ready` before taking the evidence screenshot.

### Step 5: Deployment enhancement implemented

**Enhancement:** Kubernetes liveness and readiness probes both call `/health`. Readiness prevents a pod from receiving service traffic before it responds; liveness allows Kubernetes to restart an unresponsive container. The Deployment also declares CPU/memory requests and limits.

Verify that the probes are configured and healthy:

```bash
kubectl describe deployment task-api
kubectl get pods -l app=task-api
kubectl describe pod <POD_NAME>
```

**Evidence to capture (from the assignment):**
- Ansible playbook run output.
- Dockerfile and successful image build (`docker images task-api`).
- `kubectl get pods` before and after scaling.
- `kubectl get svc task-api-service`.
- curl/browser response from the deployed API.
- Deployment/Pod description showing successful liveness and readiness probes.

## 5. Report and submission checklist

A starter report is included at `docs/DevOps_Assignment_Report.docx` and a Markdown companion at `docs/report-outline.md`. Replace every `[PLACEHOLDER]` with your details and actual evidence. Insert the real screenshots listed above; do not claim that a pipeline or deployment succeeded until you have run it successfully.

Submit all three items required by the assignment:

1. Report: title page, certificate, Abstract, Introduction, Implementation (Development Environment, Code, Description), enhancement and rationale, Results/screenshots, Conclusion and References for **each component separately**.
2. Source folder: application, tests, Jenkinsfile, `pyproject.toml`, Ansible playbook and role, Dockerfile, Kubernetes YAML, and workflow/enhancement files.
3. Repository link: update `repo_link.txt` if repository name changes, paste the URL into the report, and add the course coordinator as a repository collaborator when the coordinator's GitHub username is known.

The report is a template until the live runs and screenshots are added. Keep source code with the report; screenshots alone are not sufficient.

## Suggested resume lines (only after successful verification)

- Automated test-and-build CI for a FastAPI REST API using Jenkins SCM polling, pytest and versioned wheel artifacts.
- Configured an application service with Ansible and deployed a Dockerized API to Kubernetes with 3–5 replica scaling and HTTP liveness/readiness probes.
