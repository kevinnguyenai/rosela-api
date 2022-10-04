from sqlalchemy.orm import Session

import models, schemas

##--------------------User CRUD----------------------------
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

##--------------------Item CRUD----------------------------
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


##--------------------Recipses CRUD----------------------------
def create_recipses(db: Session, recipse: schemas.RecipesCreate):
    db_recipse = models.Recipse(**recipse.dict())
    db.add(db_recipse)
    db.commit()
    db.refresh(db_recipse)
    return db_recipse

def get_recipses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Recipse).offset(skip).limit(limit).all()

def get_recipes_id(db: Session, id: int):
    return db.query(models.Recipse).filter(models.Recipse.id==id).first()

def update_recipes_id(db: Session, id: int, data: schemas.RecipesCreate):
    _recipse = db.query(models.Recipse).filter(models.Recipse.id==id).first()
    if isinstance(_recipse, models.Recipse):
        for key, value in data:
            setattr(_recipse, key, value)
        db.add(_recipse)
        db.commit()
        db.refresh(_recipse)
    return _recipse

def delete_recipes_id(db: Session, id: int) -> bool:
    recipse = db.query(models.Recipse).filter(models.Recipse.id==id).first()
    if isinstance(recipse, models.Recipse):
        db.delete(recipse)
        db.commit()
        return True
    return False