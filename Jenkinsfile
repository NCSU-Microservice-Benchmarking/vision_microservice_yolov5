pipeline {
    // use local machine as the agent
    agent any
    // define the environment variables
    environment {
        REGISTRY = "eb2-2259-lin04.csc.ncsu.edu:28081"
        DOCKERHUB_NAMESPACE = "microservice_vision"
        APP_NAME = "vision_microservice_yolov5"
        APP_VERSION = "1.0"
    }
    stages{
        stage('Build'){
            steps{
                sh 'echo "start building the docker image"'
                sh 'docker build -t $APP_NAME .'
            }
        }
        stage('Push'){
            steps{
                sh 'echo "start pushing the docker image to docker hub"'
                // login to harbor
                withCredentials([string(credentialsId: 'harborRegistryUsername', variable: 'harborRegistryUsername'), string(credentialsId: 'harborRegistryPassword', variable: 'harborRegistryPassword')]) {
                    sh 'docker login -u $harborRegistryUsername -p $harborRegistryPassword $REGISTRY'
                }
                // tag the image
                sh 'docker tag $APP_NAME $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:$APP_VERSION'
                // push the image
                sh 'docker push $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:$APP_VERSION'
            }
        }
    }
}