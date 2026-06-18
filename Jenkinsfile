// Jenkins CI pipeline for the nepali_dating_python Django project
// Maintainer: prabeshbuilds
// Repository: https://github.com/prabeshbuilds/nepali_dating_python

pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        DJANGO_SETTINGS_MODULE = 'backend.settings'
        DOCKER_IMAGE = 'prabeshdevops/nepali_dating_python'
        DOCKER_TAG = 'latest'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/prabeshbuilds/We_Talk.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''#!/usr/bin/env bash
set -e
python3 --version
python3 -m pip install --upgrade pip
python3 -m pip install --no-cache-dir -r requirements.txt
'''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''#!/usr/bin/env bash
set -e
python3 manage.py test
'''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''#!/usr/bin/env bash
set -e
docker build -t $DOCKER_IMAGE:$DOCKER_TAG .
'''
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: env.DOCKER_CREDENTIALS_ID,
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''#!/usr/bin/env bash
set -e
docker push $DOCKER_IMAGE:$DOCKER_TAG
'''
            }
        }
    }

    post {
        success {
            echo '✅ CI pipeline completed successfully.'
        }
        failure {
            echo '❌ CI pipeline failed.'
        }
    }
}
