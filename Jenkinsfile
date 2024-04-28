pipeline {
    agent any
    stages {
        stage('Retain Clock State') {
            steps {
                sh('docker cp raspberry-clock:motor-position.txt motor-position.txt 2>/dev/null')
            }
        }
        stage('Remove Running Clock') {
            steps {
                sh('docker stop raspberry-clock || true')
                sh('docker rm raspberry-clock || true')
            }
        }
        stage('Build Image') {
            steps {
                sh('ls')
                sh('docker-compose build --no-cache')
            }
        }
        stage('Create Container') {
            steps {
                sh('docker create --name raspberry-clock --privileged --device /dev/gpiochip4 -v /dev:/dev -v /sys:/sys --restart unless-stopped -p 5005:5005 raspberry-clock_appseed-app:latest')
            }
        }
        stage('Start Clock') {
            steps {
                sh('docker start raspberry-clock')
            }
        }
        stage('Log Activity') {
            steps {
                sh('sleep 4s')
                sh('docker logs --tail 100  raspberry-clock')
            }
        }
    }
    post {
        cleanup {
            cleanWs()
        }
    }
}
