pipeline {
    agent any

    environment {
        PROJECT_DIR = "C:\\Users\\Asus\\Final-Movie_Recommendations"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                    cd ${PROJECT_DIR}
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
                """
            }
        }

        stage('Run Data Quality Checks') {
            steps {
                bat """
                    cd ${PROJECT_DIR}
                    python data_quality/checker.py
                """
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat """
                    cd ${PROJECT_DIR}
                    python -m pytest tests/ --cov=pipeline --cov-report=xml:coverage.xml --cov-report=html:coverage_report
                """
            }
        }

        stage('Run Pipeline') {
            steps {
                bat """
                    cd ${PROJECT_DIR}
                    python pipeline/main.py
                """
            }
        }

        stage('Build Report') {
            steps {
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'coverage_report',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
                junit '**/test-results.xml'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/coverage.xml', fingerprint: true
            bat """
                echo "Pipeline completed - ${currentBuild.result}"
            """
        }
        success {
            bat """
                echo "Pipeline succeeded!"
            """
        }
        failure {
            bat """
                echo "Pipeline failed!"
            """
        }
    }
}