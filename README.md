## How to run

### Dev Environment
1 - Set up your aws credentials and region
**obs.:** If you already have credentials on your local machine you can ignore this step because the Docker image is biding to your local credentials
```bash
mkdir ~/.aws

aws_data() {
cat <<EOF
[default]
region=us-east-1
aws_access_key_id=<YOUR ACCESS KEY> 
aws_secret_access_key=<YOUR SECRET KEY>
EOF
}

echo "$(aws_data)" > ~/.aws/credentials

cat ~/.aws/credentials # verify if settings are correct
```

2 - Set up the containers
```bash
docker-compose up -d --build
```

## Prod
Temp Email Software to create a new account: 
https://temp-mail.org/en


## Next Steps:
- Pagination
- Dockerfile multistage build