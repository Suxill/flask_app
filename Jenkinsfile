pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'yourdockerhubusername/flask-app:latest'  // Change to your Docker Hub repo
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'          // Jenkins Docker Hub credentials ID
        GIT_REPO = 'https://github.com/Suxill/flask_app.git'     // Your GitHub repo
    }

    stages {
        stage('Checkout') {
	   steps {
               git branch: 'main', url: "${GIT_REPO}"
	   }
        }


        stage('Setup Python') {
            steps {
                // Install virtualenv if not installed, then create and activate
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                . venv/bin/activate
                pytest tests/  # Assuming your tests are in tests/ folder
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        sh "docker push ${DOCKER_IMAGE}"
                    }
                }
            }
        }

        stage('Deploy / Run Container') {
            steps {
                // Stop and remove previous container if exists, then run new container
                sh '''
                docker stop flask-app || true
                docker rm flask-app || true
                docker run -d --name flask-app -p 8081:7000 ${DOCKER_IMAGE}
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker system prune -f'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}

