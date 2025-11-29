pipeline {
    agent any

    environment {
        // 1. Credentials ID you already have in Jenkins
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds' 
        
        // 2. Your Docker Hub Details
        DOCKER_USER = 'ullas474'
        APP_IMAGE = 'autonet-app'
        GATEWAY_IMAGE = 'autonet-gateway'
        TRAFFIC_IMAGE = 'autonet-traffic-gen'

        // 3. FORCE PATH (Critical for Mac): Ensures Jenkins finds the 'docker' command
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${env.PATH}"
    }

    stages {
        stage('Sanity Check') {
            steps {
                script {
                    // This verifies Jenkins can actually see Docker before trying to build
                    sh "docker --version"
                    echo "Docker is available!"
                }
            }
        }

        stage('Checkout Code') {
            steps {
                // Pulls the latest code from your GitHub Repo
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo '--- Building Images ---'
                    // We build all 3 services from their respective folders
                    sh "docker build -t $DOCKER_USER/$APP_IMAGE:latest ./app"
                    sh "docker build -t $DOCKER_USER/$GATEWAY_IMAGE:latest ./gateway"
                    sh "docker build -t $DOCKER_USER/$TRAFFIC_IMAGE:latest ./traffic_gen"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo '--- Logging in & Pushing ---'
                    // Securely login using your stored credentials
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        sh 'echo $PASS | docker login -u $USER --password-stdin'
                        
                        sh "docker push $DOCKER_USER/$APP_IMAGE:latest"
                        sh "docker push $DOCKER_USER/$GATEWAY_IMAGE:latest"
                        sh "docker push $DOCKER_USER/$TRAFFIC_IMAGE:latest"
                    }
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    echo '--- Removing Local Images to Save Space ---'
                    sh "docker rmi $DOCKER_USER/$APP_IMAGE:latest"
                    sh "docker rmi $DOCKER_USER/$GATEWAY_IMAGE:latest"
                    sh "docker rmi $DOCKER_USER/$TRAFFIC_IMAGE:latest"
                }
            }
        }
    }
}