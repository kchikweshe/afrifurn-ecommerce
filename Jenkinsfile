pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'afrifurn-ecommerce-api'
        DOCKER_CONTAINER = 'afrifurn-ecommerce-container'

        DOCKER_TAG = 'latest'
    }

    stages {
        stage('Setup Docker Permissions') {
            steps {
                script {
                    // Add jenkins user to docker group and fix permissions
                    sh '''
                        sudo usermod -aG docker jenkins
                        sudo chown jenkins:jenkins /home/afrifurn/.docker
                        sudo chmod 666 /var/run/docker.sock
                    '''
                }
            }
        }

        stage('Checkout') {
            steps {
                // Get code from repositor
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image with sudo
                    sh "sudo docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
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
                    // Stop existing container if it exists using sudo
                    sh '''
                        sudo docker ps -f name=${DOCKER_CONTAINER} -q | xargs --no-run-if-empty sudo docker stop
                        sudo docker ps -a -f name=${DOCKER_CONTAINER} -q | xargs --no-run-if-empty sudo docker rm
                    '''
                    
                    // Run new container with sudo
                    sh "sudo docker run -d -p 8000:8000 --name ${DOCKER_CONTAINER} ${DOCKER_IMAGE}:${DOCKER_TAG}"
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