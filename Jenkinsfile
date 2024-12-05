pipeline {
    agent any

    stages {
        stage('Install Python') {
            steps {
                sh '''
                # Update package list and install Python
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip
                '''
            }
        }
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/your-user/your-repo.git'
            }
        }
        stage('Set Up Environment') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                source venv/bin/activate
                pytest tests/
                '''
            }
        }
    }
}
