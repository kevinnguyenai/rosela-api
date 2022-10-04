from fastapi import FastAPI
from time import strftime
from typing import List
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Rosela API',
    description='Rosela API recipses',
    docs_url='/'
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##-----------users Controller--------------------
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

##----------------------Item Controller-----------------
@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

##---------------------Recipes Controller---------------
## override the exception_handler to catching custom response for RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # in case of POST creation recipses error input , will response custom as following
    if request.method == "POST" and request.__dict__.get("scope").get("path") == "/recipses":
        return JSONResponse({
            "message":"Recipse creation failed!",
            "required":"title, making_time, serves, ingredients, cost"
        }, status_code=400)
    # inherited default response for others
    return await request_validation_exception_handler(request, exc)

@app.post("/recipses", response_model=schemas.RecipesCreateResponse)
def create_recipses(recipse: schemas.RecipesCreate, db: Session = Depends(get_db)):
    db_recipse = crud.create_recipses(db, recipse)
    if isinstance(db_recipse, models.Recipse):
        created_recipse = schemas.RecipesBaseFull(
                    id=str(db_recipse.id),
                    title=db_recipse.title,
                    making_time=db_recipse.making_time,
                    serves=db_recipse.serves,
                    ingredients=db_recipse.ingredients,
                    cost=str(db_recipse.cost),
                    created_at=str(db_recipse.created_at).split(".")[0],
                    updated_at=str(db_recipse.updated_at).split(".")[0]
                )
        new_res = []
        new_res.append(created_recipse)
        return schemas.RecipesCreateResponse(
            message="Recipse successfully created!",
            recipes=new_res
        )
    raise HTTPException(
        status_code=503,
        detail={
            "message":"Recipse creation failed!",
            "required":"Internal server error when write data"
        }
    )



@app.get("/recipses", response_model=schemas.RecipesListResponse)
def get_recipses():
    pass

@app.get("recipses/{id}", response_model=schemas.RecipesResponse)
def get_recipses_by_id():
    pass

@app.patch("recipses/{id}", response_model=schemas.RecipesResponse)
def patch_recipses_by_id():
    pass

@app.delete("recipses/{id}", response_model=schemas.RecipesDeleteResponse)
def delete_recipses_by_id():
    pass
