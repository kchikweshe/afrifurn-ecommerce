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
                    sh ' docker compose down  --remove-orphans'
                    sh ' docker compose up -d'
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