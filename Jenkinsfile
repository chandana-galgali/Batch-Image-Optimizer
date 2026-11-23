// Optional Jenkins integration. Tests do not require user image files.
pipeline {
  agent any
  stages {
    stage('Install') {
      steps { sh 'python3 -m pip install -r requirements.txt' }
    }
    stage('Test') {
      steps { sh 'python3 -m unittest discover -s tests -v' }
    }
  }
}
