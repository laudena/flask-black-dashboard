pipeline {
    agent any
    stages {
        stage('Remove running clock') {
            steps {
                sh('docker stop raspberry-clock || true')
                sh('docker rm raspberry-clock || true')
            }
        }
        stage('Build image') {
            steps {
                sh('docker-compose build')
            }
        }
        stage('Create container') {
            steps {
                sh('docker create --name raspberry-clock --privileged --device /dev/gpiochip4 -v /dev:/dev -v /sys:/sys --restart unless-stopped -p 5005:5005 flask_appseed-app:latest')
            }
        }
        stage('Start clock') {
            steps {
                sh('docker start raspberry-clock')
            }
        }
        stage('Log clock activity') {
            steps {
                sh('sleep(5)')
                sh('docker logs --tail 80  raspberry-clock')
            }
        }
    }
}
