cd .. # go to the root
# users --
# push image to ecr
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 977777161073.dkr.ecr.us-east-1.amazonaws.com
docker build -t meetup-users-api -f Dockerfile.users .
docker tag meetup-users-api:latest 977777161073.dkr.ecr.us-east-1.amazonaws.com/meetup-users-api:latest
docker push 977777161073.dkr.ecr.us-east-1.amazonaws.com/meetup-users-api:latest

# force ecs to update services
aws ecs update-service --cluster meetup-cluster --service meetup-ecs-users-service --task-definition meetup-ecs-users-td --force-new-deployment