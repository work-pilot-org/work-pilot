pipeline {
    agent any

    environment {
        // Defines the docker registry or local tags if needed
        DOCKER_REGISTRY = ''
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies & Test Backend') {
            agent {
                docker { image 'python:3.13-slim' }
            }
            steps {
                sh '''
                # Install uv
                pip install uv
                # Sync dependencies and run tests
                uv sync
                uv run pytest test_*.py
                '''
            }
        }

        stage('Build Frontend') {
            agent {
                docker { image 'node:20' }
            }
            steps {
                dir('frontend') {
                    sh '''
                    npm install
                    npm run build
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                // Assuming Docker is available on the Jenkins agent
                sh 'docker-compose build'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                // Example deployment step using docker-compose
                // For a real setup, you might push to a registry and deploy remotely
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            // Clean up workspace after build
            cleanWs()
        }
    }
}
