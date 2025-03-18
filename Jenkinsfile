pipeline {
    agent any

  

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
                    echo "$USER -- $HOME"
                    // Add your test commands here
                }
            }
        }
          stage('Build') {
            steps {
                script {
                    sh 'docker compose build'
                    // Add your test commands here
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // sh 'docker stack deploy --with-registry-auth --compose-file docker-compose.yml afrifurn'
                    sh 'docker compose up'
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