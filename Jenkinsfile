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



        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    // Add your test commands here
                }
            }
        }
        stage('Login to Docker Hub') {
            steps {
                sh '''
                    docker login -u kchikweshe -p $DOCKER_PASSWORD
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker-compose up 
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    docker push kchikweshe/afrifurn-ecommerce-production:latest
                '''
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