node {
    stage('Checkout') {
        // Check out the source code from Git
        git url: 'https://github.com/<your-org>/<your-repo>.git', credentialsId: 'github-token'
    }
    stage('Build') {
        // Example: Build a Maven project
        sh 'mvn clean install'
    }
    stage('Test') {
        // Example: Run tests
        sh 'mvn test'
    }
    stage('Deploy') {
        // Example: Deploy to a server (replace with your deployment logic)
        echo 'Deploying to production...'
    }
}