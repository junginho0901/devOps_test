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
        GIT_COMMIT_SHORT = ""
        IMAGE_TAG = ""
    }
    
    stages {
        stage('Set Environment Variables') {
            steps {
                script {
                    GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
                    echo "Set IMAGE_TAG to ${IMAGE_TAG}"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        sh "docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ."
                        echo "Docker image built successfully"
                    } catch (Exception e) {
                        error "Docker 이미지 빌드 실패: ${e.message}"
                    }
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: 'admin', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                            sh "docker push ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                            echo "Docker image pushed successfully"
                        }
                    } catch (Exception e) {
                        error "Docker 이미지 푸시 실패: ${e.message}"
                    }
                }
            }
        }
        
        stage('Update Helm Chart') {
            steps {
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: 'junginho_jenkins', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                            sh """
                            sed -i 's|tag: .*|tag: "${IMAGE_TAG}"|' ./inhochart/values.yaml
                            git config user.email "cn5114555@naver.com"
                            git config user.name "junginho0901"
                            git add ./inhochart/values.yaml
                            git commit -m "Update image tag to ${IMAGE_TAG}"
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/junginho0901/devOps_test.git HEAD:main
                            """
                            echo "Helm chart updated successfully"
                        }
                    } catch (Exception e) {
                        error "Helm 차트 업데이트 실패: ${e.message}"
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
                    echo "Docker logout successful"
                } catch (Exception e) {
                    echo "Docker 로그아웃 실패: ${e.message}"
                }
            }
        }
        success {
            echo "파이프라인이 성공적으로 완료되었습니다."
        }
        failure {
            echo "파이프라인 실행 중 오류가 발생했습니다."
        }
    }
}