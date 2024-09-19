pipeline {
    agent any
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('junginho_hub')
        DOCKER_IMAGE_NAME = "jeonginho/inhorepo"
        GIT_CREDENTIALS = credentials('junginho')
    }
    stages {
        stage('Prepare') {
            steps {
                script {
                    // 워크스페이스 정리 및 Git 초기화
                    cleanWs()
                    sh "git init"
                    sh "git remote add origin https://github.com/junginho0901/devOps_test.git"
                    sh "git fetch --all"
                    sh "git checkout main"
                }
            }
        }
        stage('Set Variables') {
            steps {
                script {
                    try {
                        GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                        IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
                    } catch (Exception e) {
                        error "Failed to set variables: ${e.message}"
                    }
                }
            }
        }
        stage('Check Docker') {
            steps {
                script {
                    try {
                        sh "docker info"
                    } catch (Exception e) {
                        error "Docker is not running or not accessible: ${e.message}"
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        sh "docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ."
                    } catch (Exception e) {
                        error "Docker build failed: ${e.message}"
                    }
                }
            }
        }
        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: 'junginho_hub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                            sh "docker push ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                        }
                    } catch (Exception e) {
                        error "Failed to push Docker image: ${e.message}"
                    }
                }
            }
        }
        stage('Update Helm Chart and Push to GitHub') {
            steps {
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: 'junginho', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                            sh """
                            git pull https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/junginho0901/devOps_test.git main
                            sed -i 's|tag: .*|tag: "${IMAGE_TAG}"|' ./inhochart/values.yaml
                            git config user.email "cn5114555@naver.com"
                            git config user.name "junginho0901"
                            git add ./inhochart/values.yaml
                            git commit -m "Update image tag to ${IMAGE_TAG}"
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/junginho0901/devOps_test.git HEAD:main
                            """
                        }
                    } catch (Exception e) {
                        error "Failed to update Helm chart: ${e.message}"
                    }
                }
            }
        }
    }
    post {
        always {
            node {
                script {
                    try {
                        sh "docker logout"
                    } catch (Exception e) {
                        echo "Warning: Failed to logout from Docker: ${e.message}"
                    }
                }
            }
        }
    }
}