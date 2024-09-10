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
                    git config user.email "jenkins@example.com"
                    git config user.name "Jenkins"
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
}