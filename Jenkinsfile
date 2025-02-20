pipeline {
    agent any

    environment {
        // Update environment variables for all services
        EUREKA_IMAGE = 'afrifurn-eureka-service'
        GATEWAY_IMAGE = 'afrifurn-api-gateway-service'
        ECOMMERCE_IMAGE = 'kchikweshe/afrifurn-ecommerce-production'
        DOCKER_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // stage('Build Docker Image') {
        //     steps {
        //           sh 'docker-compose build'
        //     }
        // }

        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    // Add your test commands here
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Ensure .env file exists for docker-compose
                    // sh '''
                    //     if [ ! -f .env ]; then
                    //         echo "Error: .env file not found"
                    //         exit 1
                    //     fi
                    // '''
                    
                    // Stop existing containers and remove them
                    sh 'docker compose down --remove-orphans || true'
                    
                    // Start all services using docker-compose
                    sh 'docker compose up '
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