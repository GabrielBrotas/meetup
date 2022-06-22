
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, TypeVar
from .entities import Entity, Event

GenericEntity = TypeVar('GenericEntity', bound=Entity)

class RepositoryInterface(Generic[GenericEntity], ABC):

    @abstractmethod
    def insert(self, entity) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, entity_id: int) -> GenericEntity:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self) -> List[GenericEntity]:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity_id) -> None:
        raise NotImplementedError()

# @dataclass(slots=True)
# class EventRepository(RepositoryInterface[Event]):
#      def insert(self, entity) -> None:
#         self.items.append(entity)

#     def find_by_id(self, entity_id: int) -> Event:
#         id_str = str(entity_id)
#         return self._get(id_str)

#     def find_all(self) -> List[GenericEntity]:
#         return self.items

#     def update(self, entity) -> None:
#         entity_found = self._get(entity.id)
#         index = self.items.index(entity_found)
#         self.items[index] = entity

#     def delete(self, entity_id) -> None:
#         entity_found = self._get(entity_id)
#         self.items.remove(entity_found)

#     def _get(self, entity_id: str) -> GenericEntity:
#         entity = next(filter(lambda item: item.id == entity_id, self.items), None)

#         if not entity:
#             raise Exception(f'Entity not found using ID = {entity_id}')
#         return entity
