pipeline {
    agent { label 'windows' }

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'INFO: Installing Python dependencies from requirements.txt...'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Process Images') {
            steps {
                echo 'INFO: Executing the image optimization script...'
                bat 'python image_optimizer.py --max-width 1280 --max-height 720 --quality 85'
            }
        }
    }
    post {
        always {
            echo 'INFO: Archiving the processed images as build artifacts...'
            archiveArtifacts artifacts: 'images/output/**', followSymlinks: false
        }
    }
}