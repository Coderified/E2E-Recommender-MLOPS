pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
    }

    stages{

        stage("Cloning from Github"){
            steps{
                script{
                    echo 'Cloning from Github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Coderified-git-token', url: 'https://github.com/Coderified/E2E-Recommender-MLOPS.git']])


                }
            }
        }
        stage("Making Virt Environment in Jenkins Container"){
            steps{
                script{
                    echo 'Making Virt Envmnt in Jenkins'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''                   

                }
            }
        }

        stage('DVC Pull'){

            steps{
                withCredentials([file(credentialsId: 'gcp-key-mlops2',variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'DVC Pull'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }

    }
}