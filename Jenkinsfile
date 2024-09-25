// pipeline {
//     agent any
//     environment {
//         GIT_CREDENTIALS = credentials('junginho')
//         GIT_USERNAME = "${GIT_CREDENTIALS_USR}"
//         GIT_PASSWORD = "${GIT_CREDENTIALS_PSW}"
//         DOCKER_HUB_CREDENTIALS = credentials('junginho_hub') // Docker Hub 자격증명 ID 변경
//     }
//     options {
//         skipDefaultCheckout(true)
//     }
//     stages {
//         stage('Cleanup Workspace') {
//             steps {
//                 cleanWs()
//             }
//         }
//         stage('Checkout') {
//             steps {
//                 script {
//                     checkout([$class: 'GitSCM', 
//                         branches: [[name: '*/main']], 
//                         extensions: [
//                             [$class: 'CloneOption', depth: 1, noTags: true, shallow: true],
//                             [$class: 'CheckoutOption', timeout: 60]
//                         ], 
//                         userRemoteConfigs: [[
//                             url: 'https://github.com/junginho0901/devOps_test.git',
//                             credentialsId: 'junginho'
//                         ]]
//                     ])
//                 }
//             }
//         }
//         stage('Set Variables') {
//             steps {
//                 script {
//                     GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
//                     IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
//                 }
//             }
//         }
//         stage('Check Environment') {
//             steps {
//                 sh '''
//                     echo "Checking environment..."
//                     docker --version || echo "Docker not found"
//                     docker info || echo "Docker daemon not accessible"
//                     git --version || echo "Git not found"
//                     java -version || echo "Java not found"
//                     helm version || echo "Helm not found"
//                 '''
//             }
//         }
//         stage('Build and Push Docker Image') {  // Docker 이미지 빌드 및 푸시
//             steps {
//                 script {
//                     docker.withRegistry('https://index.docker.io/v1/', 'junginho_hub') {  // 여기에 올바른 자격증명 ID를 사용
//                         def image = docker.build("jeonginho/inhorepo:${IMAGE_TAG}")
//                         image.push()
//                     }
//                 }
//             }
//         }
//         stage('Update Helm Chart') {  // Helm 차트 업데이트
//             steps {
//                 script {
//                     sh """
//                         git config --global http.postBuffer 524288000
//                         git pull https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/junginho0901/devOps_test.git main
//                         sed -i 's|tag: .*|tag: "${IMAGE_TAG}"|' ./inhochart/values.yaml
//                         git config user.email "cn5114555@naver.com"
//                         git config user.name "junginho0901"
//                         git add ./inhochart/values.yaml
//                         git commit -m "Update image tag to ${IMAGE_TAG}"
//                         git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/junginho0901/devOps_test.git HEAD:main
//                     """
//                 }
//             }
//         }
//     }
//     post {
//         always {
//             cleanWs()
//         }
//     }
// }



pipeline {
    agent any
    environment {
        GIT_CREDENTIALS = credentials('junginho')
        GIT_USERNAME = "${GIT_CREDENTIALS_USR}"
        GIT_PASSWORD = "${GIT_CREDENTIALS_PSW}"
        DOCKER_HUB_CREDENTIALS = credentials('junginho_hub') // Docker Hub 자격증명 ID
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
                        branches: [[name: '*/main']],  // Main 브랜치 체크아웃
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
                    IMAGE_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"  // 동적 태그 생성
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
                    docker.withRegistry('https://index.docker.io/v1/', 'junginho_hub') {  // Docker Hub 인증
                        def image = docker.build("jeonginho/inhorepo:${IMAGE_TAG}")
                        image.push()  // Docker Hub로 이미지 푸시
                    }
                }
            }
        }
        stage('Update Helm Chart in Ops Branch') {  // Ops 브랜치에서 Helm 차트 업데이트
            steps {
                script {
                    sh """
                        # Ops 브랜치로 전환
                        git checkout ops
                        
                        # Ops 브랜치의 Helm 차트의 values.yaml 파일에서 이미지 태그 업데이트
                        sed -i 's|tag: .*|tag: "${IMAGE_TAG}"|' ./inhochart/values.yaml
                        
                        # Git 설정 및 변경 사항 커밋
                        git config user.email "cn5114555@naver.com"
                        git config user.name "junginho0901"
                        git add ./inhochart/values.yaml
                        git commit -m "Update image tag to ${IMAGE_TAG}"
                        
                        # Ops 브랜치에 변경 사항 푸시
                        git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/junginho0901/devOps_test.git HEAD:ops
                    """
                }
            }
        }
    }
    post {
        always {
            cleanWs()  // 워크스페이스 정리
        }
    }
}

