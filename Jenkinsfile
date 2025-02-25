pipeline {
    agent any

    environment {
        // Update environment variables for all services
        EUREKA_IMAGE = 'afrifurn-eureka-service'
        GATEWAY_IMAGE = 'afrifurn-api-gateway-service'
        ECOMMERCE_IMAGE = 'kchikweshe/afrifurn-ecommerce-production'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_IMAGE = 'kchikweshe/afrifurn-ecommerce-production'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/kchikweshe/afrifurn-ecommerce-production.git'
            }
        }

        stage('Build') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
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

        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        dockerImage.push()
                        // Also push as latest
                        dockerImage.push('latest')
                    }
                }
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
                        # Initialize swarm if not already in swarm mode
                        if [ "$(docker info | grep Swarm | grep inactive)" ]; then
                            docker swarm init || true
                        fi
                        
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