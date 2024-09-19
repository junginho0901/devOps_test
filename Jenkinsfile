pipeline {
    agent any
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('junginho_hub')
        DOCKER_IMAGE_NAME = "jeonginho/inhorepo"
        GIT_CREDENTIALS = credentials('junginho')
    }
    options {
        skipDefaultCheckout()
    }
    stages {
        stage('Cleanup Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout') {
            steps {
                script {
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/main']],
                        extensions: [
                            [$class: 'CloneOption', depth: 1, noTags: false, reference: '', shallow: true],
                            [$class: 'CheckoutOption', timeout: 30],
                            [$class: 'CleanBeforeCheckout']
                        ],
                        userRemoteConfigs: [[
                            url: 'https://github.com/junginho0901/devOps_test.git',
                            credentialsId: 'junginho'
                        ]]
                    ])
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
                        error "변수 설정 실패: ${e.message}"
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
                        error "Docker가 실행 중이 아니거나 접근할 수 없습니다: ${e.message}"
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
                        error "Docker 빌드 실패: ${e.message}"
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
                        error "Docker 이미지 푸시 실패: ${e.message}"
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
                            git config --global http.postBuffer 524288000
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
                } catch (Exception e) {
                    echo "경고: Docker 로그아웃 실패: ${e.message}"
                }
            }
        }
    }
}