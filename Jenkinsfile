
pipeline {
    agent any

    environment {
        // Docker Hub 자격 증명 사용
        DOCKER_HUB_CREDENTIALS = credentials('junginho_hub')  // 자격 증명 ID가 'junginho'로 설정됨
        DOCKER_IMAGE_NAME = "jeonginho/inhorepo"  // Docker Hub에 푸시할 이미지 이름
    }

    stages {
        stage('Cleanup Workspace') {
            steps {
                cleanWs()
        }
        }
        stage('Set Variables') {
            steps {
                script {
                    // Git 커밋 해시를 가져와서 이미지 태그로 사용
                    GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Docker 이미지를 빌드 (태그에 커밋 해시와 빌드 번호 포함)
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Docker Hub에 로그인하고 이미지를 푸시
                    withCredentials([usernamePassword(credentialsId: 'junginho_hub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Update Helm Chart and Push to GitHub') {
            steps {
                script {
                    // GitHub 자격 증명을 사용하여 Helm 차트의 이미지 태그를 업데이트하고 푸시
                    withCredentials([usernamePassword(credentialsId: 'junginho', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        sh """
                        # 최신 원격 변경 사항을 가져옴
                        git pull https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/junginho0901/devOps_test.git main

                        # Helm 차트의 values.yaml 파일에서 이미지 태그를 업데이트
                        sed -i 's|tag: .*|tag: "${IMAGE_TAG}"|' ./inhochart/values.yaml

                        # Git 커밋 설정
                        git config user.email "cn5114555@naver.com"
                        git config user.name "junginho0901"

                        # 변경 사항 커밋 및 푸시
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
            script {
                // 파이프라인 완료 후 Docker 로그아웃
                sh "docker logout"
            }
        }
    }
}