pipeline {
    agent any

    environment {
        // Credentials ID stored in Jenkins
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds' 
        
        // Your Docker Hub Username
        DOCKER_USER = 'ullas474'
        
        // Image Names
        GATEWAY_IMAGE = 'autonet-gateway'
        TRAFFIC_IMAGE = 'autonet-traffic-gen'
        ANALYZER_IMAGE = 'autonet-analyzer'
        HONEYPOT_IMAGE = 'autonet-honeypot'

        // Force Path for Mac Jenkins to find Docker
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
                    // We DO NOT build the Target App (Juice Shop) because we use the official image
                    
                    sh "docker build -t $DOCKER_USER/$GATEWAY_IMAGE:latest ./gateway"
                    sh "docker build -t $DOCKER_USER/$TRAFFIC_IMAGE:latest ./traffic_gen"
                    sh "docker build -t $DOCKER_USER/$ANALYZER_IMAGE:latest ./analyzer"
                    sh "docker build -t $DOCKER_USER/$HONEYPOT_IMAGE:latest ./honeypot"
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
                        sh "docker push $DOCKER_USER/$HONEYPOT_IMAGE:latest"
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
                    sh "docker rmi $DOCKER_USER/$HONEYPOT_IMAGE:latest"
                }
            }
        }
    }
}