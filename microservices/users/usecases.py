from dataclasses import dataclass
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

client = boto3.client('cognito-idp')

CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")


@dataclass
class ListUsersUseCase:

    def execute(self):
        response = client.list_users(
            UserPoolId=CLIENT_ID
        )
        print(response)
        return response["Users"]


@dataclass
class CreateUserUseCase:
    def execute(self, username: str, password: str, email: str) -> None:
        response = client.sign_up(
            ClientId=APP_CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
                { "Name": "email", "Value": email }
            ],
        )
        print(response)
        return None


@dataclass
class ConfirmEmailUseCase:
    def execute(self, username: str, confirmation_code: str):
        response = client.confirm_sign_up(
            ClientId=APP_CLIENT_ID,
            Username=username,
            ConfirmationCode=confirmation_code,
        )
        print(response)


@dataclass
class AuthenticateUserUseCase:
    def execute(self, username: str, password: str):
        return client.initiate_auth(
            ClientId=APP_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )


@dataclass
class GetAuthUserUseCase:
    def execute(self, access_token: str):
        return client.get_user(
            AccessToken=access_token
        )