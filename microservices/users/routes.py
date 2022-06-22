from typing import Optional, Union
from fastapi import APIRouter
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

@userRouter.post("/users")
async def create_user(item: CreateUserDTO):
    try:
        print(f'is active = {item.is_active}')
        cc_input = CreateCategoryUseCase.Input(
            name=item.name,
            description=item.description,
            is_active=item.is_active
        )

#         create_category_use_case = CreateCategoryUseCase(category_repo)

#         output = create_category_use_case.execute(input_params=cc_input)

#         return {"success": True, "category": output}
#     except Exception as error: # pylint: disable=broad-except
#         print(error)
#         return {"success": False, "error": "somethin went wrong"}