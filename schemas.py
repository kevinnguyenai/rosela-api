from lib2to3.pytree import Base
from typing import List, Union

from pydantic import BaseModel
from time import strftime


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

# compact data of recipes
class RecipesBase(BaseModel):
  id: str
  title: str
  making_time: str
  serves: str
  ingredients: str
  cost: str

# base reponse for recipes
class RecipesResponse(BaseModel):
  message: str
  recipes: Union[List[RecipesBase], None] = None

  class Config:
      orm_mode = True

# full data of recipes
class RecipesBaseFull(RecipesBase):
  created_at: str
  updated_at: str

  class Config:
      orm_mode = True

# create recipse
class RecipesCreate(BaseModel):
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: str

# created response for recipes
class RecipesCreateResponse(BaseModel):
  message: str
  recipes: Union[List[RecipesBaseFull], None] = None

#List response for recipes
class RecipesListResponse(BaseModel):
  recipes: Union[List[RecipesBase], None] = None


# delete response for recipes
class RecipesDeleteResponse(BaseModel):
  message: str