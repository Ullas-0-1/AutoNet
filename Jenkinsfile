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
        // HONEYPOT_IMAGE removed as per previous steps
        DLP_IMAGE = 'autonet-dlp'

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
                    sh "docker build -t $DOCKER_USER/$GATEWAY_IMAGE:latest ./gateway"
                    sh "docker build -t $DOCKER_USER/$TRAFFIC_IMAGE:latest ./traffic_gen"
                    sh "docker build -t $DOCKER_USER/$ANALYZER_IMAGE:latest ./analyzer"
                    // DLP Build
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
                        sh "docker push $DOCKER_USER/$DLP_IMAGE:latest"
                    }
                }
            }
        }

        stage('Deploy to K8s via Ansible') {
            steps {
                script {
                    echo '--- 🚀 Deploying via Ansible (With Vault & Roles) ---'
                    
                    // SECURITY UPGRADE:
                    // 1. Fetch the 'ansible-vault-pass' secret text from Jenkins
                    // 2. Fetch the 'k8s-config' secret file for connection
                    withCredentials([
                        string(credentialsId: 'ansible-vault-pass', variable: 'VAULT_PASS'),
                        file(credentialsId: 'k8s-config', variable: 'KUBECONFIG')
                    ]) {
                        // Create the password file dynamically
                        sh 'echo "$VAULT_PASS" > .vault_pass'
                        
                        // Run Ansible using the dynamic file
                        sh "ansible-playbook deploy.yml --vault-password-file .vault_pass"
                        
                        // Clean up immediately
                        sh "rm .vault_pass"
                    }
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    echo '--- Cleaning up ---'
                    // The || true ensures the pipeline doesn't fail if images are already gone
                    sh "docker rmi $DOCKER_USER/$GATEWAY_IMAGE:latest || true"
                    sh "docker rmi $DOCKER_USER/$TRAFFIC_IMAGE:latest || true"
                    sh "docker rmi $DOCKER_USER/$ANALYZER_IMAGE:latest || true"
                    sh "docker rmi $DOCKER_USER/$DLP_IMAGE:latest || true"
                }
            }
        }
    }
}