from dataclasses import dataclass
import boto3

client = boto3.client('cognito-idp')

@dataclass
class ListUsersUseCase:

    def execute(self):
        response = client.list_users(
            UserPoolId='us-east-1_6mdeZ0636',
            # Limit=10,
            # PaginationToken=None
        )
        print(response)
        return response["Users"]

@dataclass
class CreateUserUseCase:

    def execute(username: str, password: str, email: str) -> None:
        response = client.