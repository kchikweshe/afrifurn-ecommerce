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


        stage('Build Docker Image') {
            steps {
                sh '''
                    docker buildx build . -t kchikweshe/afrifurn-ecommerce-production:latest
                '''
            }
        }
        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push kchikweshe/afrifurn-ecommerce-production:latest
                '''
            }
        }

        stage('Swarm Init') {
            steps {
                sh '''
                        # Initialize swarm if not already in swarm mode
                        if [ "$(docker info | grep Swarm | grep inactive)" ]; then
                            docker swarm init || true
                        fi                '''
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh '''
          
                        docker-compose up -d
                 
                    '''
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