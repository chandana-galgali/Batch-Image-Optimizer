pipeline {
    agent { label 'windows' }
    stages {
        stage('Build') {
            steps {
                echo 'BUILD STAGE: Installing project dependencies...'
                bat 'python -m pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                echo 'TEST STAGE: Running the image optimizer to validate the script...'
                bat 'python image_optimizer.py --max-width 800 --max-height 600 --quality 75'
            }
        }
        stage('Deploy') {
            steps {
                echo 'DEPLOY STAGE: Archiving the optimized images as build artifacts...'
                archiveArtifacts artifacts: 'images/output/**', followSymlinks: false
            }
        }
    }
    post {
        always {
            echo 'PIPELINE END: Cleaning up the workspace.'
            cleanWs() 
        }
    }
}