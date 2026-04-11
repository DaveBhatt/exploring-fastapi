from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Hash the user's password before saving it to the database
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump()) # Use model_dump instead of deprecated dict method to convert the Pydantic model to a dictionary.
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Refresh the instance to get the generated ID and other fields from the database
    return new_user # Return the new user without the password field, as defined in the UserOut schema.

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found!")
    
    return user