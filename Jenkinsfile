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

                    sh 'docker stack deploy --compose-file docker-compose.yml afrifurn-stack'
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
            sh 'docker stack rm afrifurn-stack'
            sh 'docker-compose down'
        }
        always {
            cleanWs()
        }
    }
} 