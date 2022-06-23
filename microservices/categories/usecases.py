from dataclasses import dataclass
from typing import Union
from sqlalchemy.orm import Session
from sqlalchemy import update
import models
import eventing

@dataclass
class ListCategoriesUseCase:
    db: Session

    def execute(self):
        return self.db.query(models.Category).all()


@dataclass
class CreateCategoryUseCase:
    db: Session

    def execute(self, name: str) -> None:
        category = models.Category(name=name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        print(category)


@dataclass
class GetCategoryByIdUseCase:
    db: Session

    def execute(self, category_id: Union[int, str]):
        return self.db.query(models.Category).get(int(category_id))

@dataclass
class UpdateCategoryNameUseCase:
    db: Session
    eventing: eventing.CategoryEvents

    def execute(self, category_id: Union[int, str], name: str):
        stmt = update(models.Category).where(models.Category.id == category_id).values(name=name).\
            execution_options(synchronize_session="fetch")
        self.db.execute(stmt)
        self.db.commit()

        self.eventing.category_renamed(category_id, name)
        return