node {
    def app

    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
        app = docker.build("kchikweshe/afrifurn-ecommerce-production")
    }

    stage('Test image') {
        app.inside {
            sh 'echo "Tests passed"'
            // Add your actual test commands here
        }
    }

    stage('Push image') {
        docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
            app.push("${env.BUILD_NUMBER}")
            app.push('latest')
        }
    }

    stage('Deploy') {
        sh '''
            # Initialize swarm if not already in swarm mode
            if [ "$(docker info | grep Swarm | grep inactive)" ]; then
                docker swarm init || true
            fi
            
            docker-compose up -d
        '''
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