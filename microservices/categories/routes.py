from typing import Optional, Union
from fastapi import APIRouter, Header, Depends, status, Response
from pydantic import BaseModel
import usecases
from sqlalchemy.orm import Session
import database

categoriesRouter = APIRouter(
    tags=["category"]
)

@categoriesRouter.get("/categories")
async def list_categories(db: Session = Depends(database.get_db)):
    try:
        list_categories_use_case = usecases.ListCategoriesUseCase(db)

        categories = list_categories_use_case.execute()

        return {"success": True, "categories": categories}
    except Exception as error:
        print(error)
        return {"success": False, "error": str(error)}

class CreateCategoryDTO(BaseModel):
    name: str

# TODO: verify if the user is admin
@categoriesRouter.post("/category")
async def create_category(item: CreateCategoryDTO, db: Session = Depends(database.get_db)):
    try:
        create_category_use_case = usecases.CreateCategoryUseCase(db)

        create_category_use_case.execute(
            name=item.name
        )

        return {"success": True}
    except Exception as error:
        print(error)
        return {"success": False, "error": str(error)}


@categoriesRouter.get("/category/{category_id}")
async def get_category(category_id: int, response: Response, db: Session = Depends(database.get_db)):
    try:
        get_category_use_case = usecases.GetCategoryByIdUseCase(db)

        result = get_category_use_case.execute(
            category_id=category_id
        )

        if result == None:
            raise Exception("Category with id: {} not found".format(category_id))

        return {"success": True, "category": result}
    except Exception as error:
        print(error)
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"success": False, "error": str(error)}
