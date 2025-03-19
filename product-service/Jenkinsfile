pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                script {
                    sh 'sudo docker-compose build'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh 'sudo docker-compose down  --remove-orphans'
                    sh 'sudo docker-compose up -d'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! All services are deployed.'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
        always {
            cleanWs()
        }
    }
} 