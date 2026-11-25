pipeline {
    agent any
    options {
        timestamps()
        disableConcurrentBuilds()
    }
    triggers {
        // Polling demonstrates automatic CI without requiring a publicly reachable webhook.
        pollSCM('H/2 * * * *')
    }
    environment {
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PYTHONDONTWRITEBYTECODE = '1'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Setup Python') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && python -m pip install --upgrade pip'
                sh '. .venv/bin/activate && pip install -r requirements-dev.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'mkdir -p test-results'
                sh '. .venv/bin/activate && pytest --junitxml=test-results/pytest.xml'
            }
        }
        stage('Build') {
            steps {
                sh '. .venv/bin/activate && python -m build --wheel'
                sh '''
                  set -eu
                  mkdir -p artifacts
                  SHA="$(git rev-parse --short=7 HEAD)"
                  WHEEL="$(find dist -maxdepth 1 -name '*.whl' -print -quit)"
                  test -n "$WHEEL"
                  cp "$WHEEL" "artifacts/task-api-${BUILD_NUMBER}-${SHA}.whl"
                  printf 'build=%s\ncommit=%s\n' "$BUILD_NUMBER" "$SHA" > artifacts/build-info.txt
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'artifacts/*', fingerprint: true, allowEmptyArchive: true
            junit testResults: 'test-results/*.xml', allowEmptyResults: true
        }
        success { echo 'Task API CI pipeline passed.' }
        failure { echo 'Task API CI pipeline failed; inspect the stage console output.' }
    }
}
