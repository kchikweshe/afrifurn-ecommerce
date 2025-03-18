pipeline {
    agent any

  

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Docker Permissions') {
            steps {
                script {
                    sh 'sudo chown afrifurn:docker ~/.docker || mkdir -p ~/.docker && sudo chown afrifurn:docker ~/.docker'
                    sh 'id'  // Print user info for verification
                }
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
                    echo "$USER -- $HOME"
                    // Add your test commands here
                }
            }
        }
          stage('Build') {
            steps {
                script {
                    sh 'docker compose -f docker-compose.yml build'
                    // Add your test commands here
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // sh 'docker stack deploy --with-registry-auth --compose-file docker-compose.yml afrifurn'
                    sh 'docker compose up -d'
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