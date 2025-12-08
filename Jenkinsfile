pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds' 
        DOCKER_USER = 'ullas474'
        
        GATEWAY_IMAGE = 'autonet-gateway'
        TRAFFIC_IMAGE = 'autonet-traffic-gen'
        ANALYZER_IMAGE = 'autonet-analyzer'
        HONEYPOT_IMAGE = 'autonet-honeypot'
        DLP_IMAGE = 'autonet-dlp'  // NEW IMAGE

        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${env.PATH}"
    }

    stages {
        stage('Sanity Check') {
            steps {
                script {
                    sh "docker --version"
                    echo "Docker is ready!"
                }
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo '--- Building Microservices ---'
                    sh "docker build -t $DOCKER_USER/$GATEWAY_IMAGE:latest ./gateway"
                    sh "docker build -t $DOCKER_USER/$TRAFFIC_IMAGE:latest ./traffic_gen"
                    sh "docker build -t $DOCKER_USER/$ANALYZER_IMAGE:latest ./analyzer"
                    // NEW BUILD STEP
                    sh "docker build -t $DOCKER_USER/$DLP_IMAGE:latest ./dlp"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo '--- Logging in & Pushing ---'
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        sh 'echo $PASS | docker login -u $USER --password-stdin'
                        
                        sh "docker push $DOCKER_USER/$GATEWAY_IMAGE:latest"
                        sh "docker push $DOCKER_USER/$TRAFFIC_IMAGE:latest"
                        sh "docker push $DOCKER_USER/$ANALYZER_IMAGE:latest"
                        // NEW PUSH STEP
                        sh "docker push $DOCKER_USER/$DLP_IMAGE:latest"
                    }
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    echo '--- Cleaning up ---'
                    sh "docker rmi $DOCKER_USER/$GATEWAY_IMAGE:latest"
                    sh "docker rmi $DOCKER_USER/$TRAFFIC_IMAGE:latest"
                    sh "docker rmi $DOCKER_USER/$ANALYZER_IMAGE:latest"
                    sh "docker rmi $DOCKER_USER/$DLP_IMAGE:latest"
                }
            }
        }
    }
}