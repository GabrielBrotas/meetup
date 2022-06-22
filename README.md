## How to run

### Dev Environment
1 - Set up your aws credentials and region
```bash
mkdir ~/.aws

aws_data() {
cat <<EOF
[default]
region=us-east-1
aws_access_key_id = <YOUR ACCESS KEY> 
aws_secret_access_key = <YOUR SECRET KEY>
EOF
}

echo "$(aws_data)" > ~/.aws/credentials

cat ~/.aws/credentials # verify if settings are correct
```