pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = 'rugged-sentry-454806-a8'
        GCLOUD_PATH = "/var/jenkins_home/gcloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
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
        stage('Build and Push Image to GCR'){

            steps{
                withCredentials([file(credentialsId: 'gcp-key-mlops2',variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Build and Push Image to GCR'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file ${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials mlops-2-cluster --region us-central1 
                        kubectl apply -f deployement.yaml 
                        '''
                    }
                }
            }
        }
        stage('Kubernetes Deployment'){

            steps{
                withCredentials([file(credentialsId: 'gcp-key-mlops2',variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Kubernetes Deployment'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        glcoud auth activate-service-account --key-file ${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        glcoud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/e2e-recommender-mlops:latest .
                        docker push gcr.io/${GCP_PROJECT}/e2e-recommender-mlops:latest
                        '''
                    }
                }
            }
        }

    }
}