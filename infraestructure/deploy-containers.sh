# TODO: terraform create this sh file using file provider

cd .. # go to the root

# users ---
# push image to ecr
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 977777161073.dkr.ecr.us-east-1.amazonaws.com
docker build -t meetup-users-api -f Dockerfile.users .
docker tag meetup-users-api:latest 977777161073.dkr.ecr.us-east-1.amazonaws.com/meetup-users-api:latest
docker push 977777161073.dkr.ecr.us-east-1.amazonaws.com/meetup-users-api:latest

aws ecs update-service --cluster meetup-cluster --service meetup-ecs-users-service --task-definition meetup-ecs-users-td --force-new-deployment

# categories ---
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 977777161073.dkr.ecr.us-east-1.amazonaws.com
docker build -t meetup-categories-api -f Dockerfile.categories .
docker tag meetup-categories-api:latest 977777161073.dkr.ecr.us-east-1.amazonaws.com/meetup-categories-api:latest
docker push 977777161073.dkr.ecr.us-east-1.amazonaws.com/meetup-categories-api:latest

aws ecs update-service --cluster meetup-cluster --service meetup-ecs-categories-service --task-definition meetup-ecs-categories-td --force-new-deployment

# meetings ---
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 977777161073.dkr.ecr.us-east-1.amazonaws.com
docker build -t meetup-meetings-api -f Dockerfile.meetings .
docker tag meetup-meetings-api:latest 977777161073.dkr.ecr.us-east-1.amazonaws.com/meetup-meetings-api:latest
docker push 977777161073.dkr.ecr.us-east-1.amazonaws.com/meetup-meetings-api:latest

aws ecs update-service --cluster meetup-cluster --service meetup-ecs-meetings-service --task-definition meetup-ecs-meetings-td --force-new-deployment
