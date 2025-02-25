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
                    sh '''
                        # Debug information
                        echo "Docker version:"
                        docker --version
                        echo "Docker Swarm status:"
                        docker info | grep Swarm
                        
                        // # Initialize swarm if not already in swarm mode
                        // if [ "$(docker info | grep Swarm | grep inactive)" ]; then
                        //     docker swarm init || true
                        // fi
                        # Deploy the stack
                        // docker stack deploy -c docker-compose.yml afrifurn --with-registry-auth
                        docker-compose up -d
                        # Wait a bit and check stack status
                        // sleep 10
                        // docker stack ps afrifurn
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