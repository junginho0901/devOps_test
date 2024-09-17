// pipeline {
//     agent any
//     environment {
//         DOCKER_HUB_CREDENTIALS = credentials('admin')
//         DOCKER_IMAGE_NAME = "jeonginho/inhorepo"
//         DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
//     }
//     stages {
//         stage('Build Docker Image') {
//             steps {
//                 sh "docker build --no-cache -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ."
//             }
//         }
//         stage('Push Docker Image') {
//             steps {
//                 script {
//                     withCredentials([usernamePassword(credentialsId: 'admin', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
//                         sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
//                         sh "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
//                         sh "docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:latest"
//                         sh "docker push ${DOCKER_IMAGE_NAME}:latest"
//                     }
//                 }
//             }
//         }
//     }
//     post {
//         always {
//             sh "docker logout"
//         }
//     }
// }


// pipeline {
//     agent any
//     environment {
//         DOCKER_HUB_CREDENTIALS = credentials('admin')
//         DOCKER_IMAGE_NAME = "jeonginho/inhorepo"
//         GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
//         IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
//     }
//     stages {
//         stage('Build Docker Image') {
//             steps {
//                 sh "docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ."
//             }
//         }
//         stage('Push Docker Image') {
//             steps {
//                 script {
//                     withCredentials([usernamePassword(credentialsId: 'admin', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
//                         sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
//                         sh "docker push ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
//                     }
//                 }
//             }
//         }
//         stage('Update Helm Chart') {
//             steps {
//                 script {
//                     // GitHub 자격 증명을 사용하여 git pull 및 git push 수행
//                     withCredentials([usernamePassword(credentialsId: 'junginho_jenkins', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
//                         // 먼저 최신 원격 변경 사항을 가져옴
//                         sh """
//                         git pull https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/junginho0901/devOps_test.git main
//                         sed -i 's|tag: .*|tag: "${IMAGE_TAG}"|' ./inhochart/values.yaml
//                         git config user.email "cn5114555@naver.com"
//                         git config user.name "junginho0901"
//                         git add ./inhochart/values.yaml
//                         git commit -m "Update image tag to ${IMAGE_TAG}"
//                         git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/junginho0901/devOps_test.git HEAD:main
//                         """
//                     }
//                 }
//             }
//         }
//     }
//     post {
//         always {
//             sh "docker logout"
//         }
//     }
// }
pipeline {
    agent any
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('admin')
        DOCKER_IMAGE_NAME = "jeonginho/inhorepo"
        GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
    }
    stages {
        stage('Initialize') {
            steps {
                script {
                    echo "Initializing pipeline..."
                    echo "Image tag set to: ${IMAGE_TAG}"
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        echo "Building Docker image..."
                        sh "docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ."
                        echo "Docker image built successfully"
                    } catch (Exception e) {
                        error "Failed to build Docker image: ${e.message}"
                    }
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    try {
                        echo "Pushing Docker image to registry..."
                        withCredentials([usernamePassword(credentialsId: 'admin', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                            sh "docker push ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                        }
                        echo "Docker image pushed successfully"
                    } catch (Exception e) {
                        error "Failed to push Docker image: ${e.message}"
                    }
                }
            }
        }
        stage('Update Helm Chart') {
            steps {
                script {
                    try {
                        echo "Updating Helm chart..."
                        withCredentials([usernamePassword(credentialsId: 'junginho_jenkins', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
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
                        echo "Helm chart updated successfully"
                    } catch (Exception e) {
                        error "Failed to update Helm chart: ${e.message}"
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                try {
                    sh "docker logout"
                    echo "Docker logged out successfully"
                } catch (Exception e) {
                    echo "Warning: Failed to logout from Docker: ${e.message}"
                }
            }
        }
        success {
            echo "Pipeline executed successfully"
        }
        failure {
            echo "Pipeline execution failed"
        }
    }
}