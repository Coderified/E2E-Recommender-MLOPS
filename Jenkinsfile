pipeline{
    agent any

    stages{

        stage("Cloning from Github"){
            steps{
                script{
                    echo 'Cloning from Github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Coderified-git-token', url: 'https://github.com/Coderified/E2E-Recommender-MLOPS.git']])


                }
            }
        }

    }
}