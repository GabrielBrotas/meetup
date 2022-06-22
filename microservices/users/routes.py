from typing import Optional, Union
from fastapi import APIRouter, Header
from pydantic import BaseModel # pylint: disable=no-name-in-module
import usecases

userRouter = APIRouter(
    tags=["user"]
)

@userRouter.get("/users")
async def list_users():
    try:
        list_users_use_case = usecases.ListUsersUseCase()

        users = list_users_use_case.execute()

        return {"success": True, "users": users}
    except Exception as error:
        print(error)
        return {"success": False, "error": str(error)}

class CreateUserDTO(BaseModel):
    username: str
    password: str
    email: str

@userRouter.post("/users/sign-up")
async def create_user(item: CreateUserDTO):
    try:
        create_user_use_case = usecases.CreateUserUseCase()

        create_user_use_case.execute(
            username=item.username,
            password=item.password,
            email=item.email,
        )

        return {"success": True}
    except Exception as error:
        print(error)
        return {"success": False, "error": str(error)}

class ConfirmEmailUserDTO(BaseModel):
    username: str
    confirmation_code: str

@userRouter.post("/users/sign-up/confirm")
async def confirm_email(item: ConfirmEmailUserDTO):
    try:
        confirm_email_use_case = usecases.ConfirmEmailUseCase()

        confirm_email_use_case.execute(
            username=item.username,
            confirmation_code=item.confirmation_code
        )

        return {"success": True}
    except Exception as error:
        print(error)
        return {"success": False, "error": str(error)}


class SignInUserDTO(BaseModel):
    username: str
    password: str

@userRouter.post("/users/sign-in")
async def auth_user(item: SignInUserDTO):
    try:
        auth_user_use_case = usecases.AuthenticateUserUseCase()

        result = auth_user_use_case.execute(
            username=item.username,
            password=item.password,
        )

        return {"success": True, "result": result}
    except Exception as error:
        print(error)
        return {"success": False, "error": str(error)}


@userRouter.get("/users/me")
async def get_me(authorization: Union[str, None] = Header(default=None)):
    try:
        get_auth_user_use_case = usecases.GetAuthUserUseCase()

        result = get_auth_user_use_case.execute(
            access_token=authorization
        )

        return {"success": True, "result": result}
    except Exception as error:
        print(error)
        return {"success": False, "error": str(error)}
