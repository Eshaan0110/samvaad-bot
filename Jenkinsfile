pipeline {
    agent any

    environment {
        IMAGE_NAME = "sanskrit-chatbot"
        IMAGE_TAG  = "jenkins"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Eshaan0110/samvaad-bot.git'
            }
        }

        stage('Setup uv') {
            steps {
                echo 'Verifying uv installation...'
                bat 'uv --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing project dependencies with uv...'
                bat 'uv sync'
            }
        }

        stage('Validate') {
            steps {
                echo 'Compiling app.py to catch syntax errors...'
                bat 'uv run python -m py_compile app.py'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
                bat "docker images %IMAGE_NAME%"
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check the console output above.'
        }
    }
}
