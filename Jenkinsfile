pipeline {
    agent any

    environment {
        // Update environment variables for all services
        EUREKA_IMAGE = 'afrifurn-eureka-service'
        GATEWAY_IMAGE = 'afrifurn-api-gateway-service'
        ECOMMERCE_IMAGE = 'kchikweshe/afrifurn-ecommerce-production'
        DOCKER_TAG = 'latest'
        DOCKER_CREDS = credentials('docker-hub-credentials')
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
                    sh 'whoami'
                    // Add your test commands here
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    try {
                        parallel(
                            eureka: {
                                sh "docker build -t ${EUREKA_IMAGE}:${DOCKER_TAG} ./eureka-service"
                            },
                            gateway: {
                                sh "docker build -t ${GATEWAY_IMAGE}:${DOCKER_TAG} ./api-gateway"
                            },
                            ecommerce: {
                                sh "docker build -t ${ECOMMERCE_IMAGE}:${DOCKER_TAG} ."
                            }
                        )
                    } catch (Exception e) {
                        error "Failed to build Docker images: ${e.message}"
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    try {
                        sh '''
                            docker login -u ${DOCKER_CREDS_USR} -p ${DOCKER_CREDS_PSW}
                            docker push ${ECOMMERCE_IMAGE}:${DOCKER_TAG}
                        '''
                    } catch (Exception e) {
                        error "Failed to push Docker image: ${e.message}"
                    }
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
