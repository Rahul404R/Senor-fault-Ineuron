with specific access

1. EC2 access: It is virtual machine
2. Create IAM user for deployment

with specific access:

1. EC2 access: It is virtual machine
2. S3 Bucket: To store artifact and model in s3 bucket
3. ECR: Elastic Container registry
To save your docker image in aws

Policy names
1. AmazonEC2FullAccess
2. AmazonEC2ContainerRegistryFullAccess
3. AmazonS3FullAccess


Description: About the Deployment

1. Build docker image of the source code
2. Push your docker image to ECR
3. Launch your EC2
4. Pull your image from ECR in EC2
5. Launch your docker image in EC2

STEPS

1. Create a S3 bucket in ap-sourth-1

	BUCKET NAME - sensor-fault-detect-pipeline

2. Create ECR repo to store/save docker image
	REPO - 423253052430.dkr.ecr.ap-south-1.amazonaws.com/sensor-fault-model

3. EC2 machine Ubuntu created
4. Open EC2 and Install docker in EC2 machine

commands:
sudo apt-get update -y
sudo apt-get upgrade

curl -fsSL https://get.doker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker

5. Configure EC2 a self-hosted runner to acces github actions
settings-> actions-> runner-> new self hosted runner-> choose os based on vm 
then run the commands one by one

to run the git actions in vm run command -> ./run.sh

6.Setup Github Secret Keys
	AWS_ACCESS_KEY_ID
	AWS_SECRET_ACCESS_KEY
	AWS_REGION
	AWS_ECR_LOGIN_URI
	ECR_REPOSITORY_NAME
	MONGO_DB_URL
