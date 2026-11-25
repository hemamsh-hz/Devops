# DevOps Assignment Report — Task Management API

> Complete the fields and insert actual screenshots/output before submission. The assignment requires a separate write-up for each component.

## Title page
- Institution: [INSTITUTION NAME]
- Department: [DEPARTMENT]
- Course: DevOps — 25CIAEC59 / 25CYAEC59
- Project: Task Management API — CI/CD Pipeline and Kubernetes Deployment
- Student name: [STUDENT NAME]
- USN: [USN]
- Academic year/semester: [DETAILS]
- Submitted to: [FACULTY NAME]

## Certificate
This is to certify that the project report entitled **Task Management API — CI/CD Pipeline and Kubernetes Deployment** is submitted by [STUDENT NAME], [USN], in partial fulfilment of the requirements for the DevOps course 25CIAEC59 / 25CYAEC59. The work and implementation evidence are to be reviewed by the course instructor.

Faculty signature: [SIGNATURE] · Date: [DATE]

## Component 1 — CI pipeline (10 marks)

### Abstract
This component demonstrates a basic CI workflow for a Task Management REST API. Git provides source control and feature-branch history, while Jenkins checks out changes, installs dependencies, runs pytest, builds a Python wheel, and archives the artifact with build and commit identifiers. A GitHub Actions workflow provides a second CI run.

### Introduction
The goal is to automate build verification when source code changes, reducing manual work and identifying regressions before an artifact is used for deployment.

### Implementation
**Development environment:** [OS], Python [VERSION], Git [VERSION], Jenkins [VERSION], pytest [VERSION].  
**Code:** `app/main.py`, `tests/test_api.py`, `pyproject.toml`, `Jenkinsfile`, `.github/workflows/ci.yml`.  
**Description:** FastAPI exposes `/`, `/health`, `GET /todos`, `POST /todos`, and `GET /todos/{task_id}`. Jenkins checks out the repository, installs the development requirements, runs four tests, builds a wheel, and archives a versioned artifact. SCM polling makes the job detect new commits.

**CI enhancement and rationale:** Automated pytest tests run before the build; versioned artifact filenames contain the Jenkins build number and short commit SHA. The tests help catch errors before packaging, and versioning makes an artifact traceable to a source revision.

### Results
- [INSERT SCREENSHOT 1: Git branches and merge history]
- [INSERT SCREENSHOT 2: Jenkins SCM and polling configuration]
- [INSERT SCREENSHOT 3: Successful Jenkins console output]
- [INSERT SCREENSHOT 4: Archived versioned wheel]
- [INSERT SCREENSHOT 5: Passing tests or GitHub Actions run]

Observed result: [RECORD ONLY THE ACTUAL BUILD NUMBER, TEST RESULT AND ARTIFACT NAME].

### Conclusion
[Summarize what you successfully configured and verified. Mention any limitation honestly.]

### References
- Python documentation: https://docs.python.org/3/
- FastAPI documentation: https://fastapi.tiangolo.com/
- Jenkins User Documentation: https://www.jenkins.io/doc/
- GitHub Actions documentation: https://docs.github.com/actions

## Component 2 — Ansible, Docker and Kubernetes deployment (10 marks)

### Abstract
This component reuses the Task Management REST API and configures a Linux host with Ansible. A Docker image packages the application, and Kubernetes runs it as three replicas behind a Service. Scaling is demonstrated by increasing to five replicas and returning to three. Kubernetes health probes are the deployment enhancement.

### Introduction
Configuration management and container orchestration help make deployments repeatable. Ansible captures host setup as code, Docker packages application dependencies, and Kubernetes maintains the desired number of running replicas.

### Implementation
**Development environment:** [OS/VM], Ansible [VERSION], Docker [VERSION], Kubernetes/Minikube or Kind [VERSION].  
**Code:** `ansible/playbook.yml`, `ansible/roles/task_api/`, `Dockerfile`, `k8s/deployment.yaml`, `k8s/service.yaml`.  
**Description:** The playbook installs Python, creates an application account and directory, copies application source and requirements, creates a virtual environment, installs dependencies, and manages a systemd service. The Dockerfile builds the application wheel in a builder stage and runs it in a slim runtime stage as a non-root user. The Kubernetes Deployment defines three replicas, while the Service routes requests to matching `app: task-api` pods.

**Deployment enhancement and rationale:** Both liveness and readiness probes query `/health`. This provides an automated health signal to Kubernetes and helps avoid sending traffic to pods that are not ready.

### Results
- [INSERT SCREENSHOT 1: Successful ansible-playbook run]
- [INSERT SCREENSHOT 2: Docker image build and image listing]
- [INSERT SCREENSHOT 3: Three running pods]
- [INSERT SCREENSHOT 4: Five running pods after scaling]
- [INSERT SCREENSHOT 5: Service details and successful curl/browser request]
- [INSERT SCREENSHOT 6: Liveness/readiness probe details]

Observed result: [RECORD ACTUAL POD COUNTS, SERVICE ENDPOINT AND HEALTH CHECK RESPONSE].

### Conclusion
[Summarize only what was actually run and verified.]

### References
- Ansible documentation: https://docs.ansible.com/
- Docker documentation: https://docs.docker.com/
- Kubernetes documentation: https://kubernetes.io/docs/
- Minikube documentation: https://minikube.sigs.k8s.io/docs/
