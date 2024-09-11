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


pipeline {
    agent any
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('admin')
        DOCKER_IMAGE_NAME = "jeonginho/inhorepo"
        GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
    }
    stages {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'admin', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }
        stage('Update Helm Chart') {
            steps {
                script {
                    // Helm 차트의 values.yaml 파일 업데이트
                    sh """
                    sed -i 's|tag: .*|tag: "${IMAGE_TAG}"|' ./inhochart/values.yaml
                    git config user.email "cn5114555@naver.com"
                    git config user.name "junginho0901"
                    git add ./inhochart/values.yaml
                    git commit -m "Update image tag to ${IMAGE_TAG}"
                    git push origin HEAD:main
                    """
                }
            }
        }
    }
    post {
        always {
            sh "docker logout"
        }
    }
}pipeline {
    agent any
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('admin')
        DOCKER_IMAGE_NAME = "jeonginho/inhorepo"
        GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
    }
    stages {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'admin', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }
        stage('Update Helm Chart') {
            steps {
                script {
                    // GitHub 자격 증명을 사용하여 git push 수행
                    withCredentials([usernamePassword(credentialsId: 'github-credentials', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        sh """
                        sed -i 's|tag: .*|tag: "${IMAGE_TAG}"|' ./inhochart/values.yaml
                        git config user.email "cn5114555@naver.com"
                        git config user.name "junginho0901"
                        git add ./inhochart/values.yaml
                        git commit -m "Update image tag to ${IMAGE_TAG}"
                        git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/junginho0901/devOps_test.git HEAD:main
                        """
                    }
                }
            }
        }
    }
    post {
        always {
            sh "docker logout"
        }
    }
}
