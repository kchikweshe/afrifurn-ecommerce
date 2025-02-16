pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'afrifurn-ecommerce-api'
        DOCKER_CONTAINER = 'afrifurn-ecommerce-container'

        DOCKER_TAG = 'latest'
        DOCKER_SOCKET = 'usermod -aG docker jenkins'
    }

    stages {
  

        stage('Checkout') {
            steps {
                // Get code from repositor
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh "docker  build --tag ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Add your test commands here
                    echo 'Running tests...'
                    // Example: sh 'python -m pytest'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Stop existing container if it exists
                    sh '''
                        docker ps -f name=${DOCKER_CONTAINER} -q | xargs --no-run-if-empty docker stop
                        docker ps -a -f name=${DOCKER_CONTAINER} -q | xargs --no-run-if-empty docker rm
                    '''
                    
                    // Run new container
                    sh "docker run -d -p 8000:8000 --name ${DOCKER_CONTAINER} ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Application is deployed.'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details..'
        }
        always {
            // Clean up workspace
            cleanWs()
        }
    }
} 