from abc import abstractmethod
from dataclasses import dataclass
from typing import Union
from sqlalchemy.orm import Session
import models

@dataclass
class ListMeetingsUseCase:
    db: Session

    def execute(self):
        return self.db.query(models.Meeting).all()


@dataclass
class CreateCategoryUseCase:
    db: Session

    def execute(self, name: str) -> None:
        category = models.Category(name=name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        print(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        def __post_init__(self):
            if not self.is_active:
                object.__setattr__(self, 'is_active', Category.get_field('is_active').default)

        name: str
        # get the default values from the entity because it can change
        description: Optional[str] = Category.get_field('description').default
        is_active: Optional[bool] = Category.get_field('is_active').


@dataclass
class GetCategoryByIdUseCase:
    db: Session

    def execute(self, category_id: Union[int, str]):
        return self.db.query(models.Category).get(int(category_id))