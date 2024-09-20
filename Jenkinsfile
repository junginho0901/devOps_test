pipeline {
    agent any
    environment {
        GIT_CREDENTIALS = credentials('junginho')
        GIT_USERNAME = "${GIT_CREDENTIALS_USR}"
        GIT_PASSWORD = "${GIT_CREDENTIALS_PSW}"
        DOCKER_HUB_CREDENTIALS = credentials('junginho_hub') // Docker Hub 자격증명 ID 변경
    }
    options {
        skipDefaultCheckout(true)
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
                            [$class: 'CloneOption', depth: 1, noTags: true, shallow: true],
                            [$class: 'CheckoutOption', timeout: 60]
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
                    GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
                }
            }
        }
        stage('Check Environment') {
            steps {
                sh '''
                    echo "Checking environment..."
                    docker --version || echo "Docker not found"
                    docker info || echo "Docker daemon not accessible"
                    git --version || echo "Git not found"
                    java -version || echo "Java not found"
                    helm version || echo "Helm not found"
                '''
            }
        }
        stage('Build and Push Docker Image') {  // Docker 이미지 빌드 및 푸시
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'junginho_hub') {  // 여기에 올바른 자격증명 ID를 사용
                        def image = docker.build("jeonginho/inhorepo:${IMAGE_TAG}")
                        image.push()
                    }
                }
            }
        }
        stage('Update Helm Chart') {
            steps {
                script {
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
            }
        }
        stage('Deploy to Kubernetes') {  // Helm 배포
            steps {
                script {
                    sh """
                    helm upgrade --install myapp ./inhochart --namespace project-services --values ./inhochart/values.yaml
                    """
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
