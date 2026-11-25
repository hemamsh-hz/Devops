# Jenkins SCM Polling

The Task API uses Jenkins Pipeline for continuous integration.

The pipeline automatically checks the GitHub main branch using
SCM polling every two minutes.

Each detected change triggers:
1. Repository checkout
2. Python environment setup
3. Automated pytest execution
4. Python wheel build
5. Versioned artifact archiving
