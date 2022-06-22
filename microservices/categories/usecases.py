from dataclasses import dataclass
from typing import Union
from sqlalchemy.orm import Session
import models

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