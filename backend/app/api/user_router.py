from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from requests import Session
from app.services.user_service import insert_user_data
from app.core.database import get_db
from app.services.user_service import insert_user_data
from app.schemas.user_schema import UserUpdate

router = APIRouter(prefix="/user", tags=["user"])

@router.post(
    "/",
    summary="Register or update user data"
    )
def user_data(user: UserUpdate, db: Session = Depends(get_db)):
    """
    Registers or updates user data in the database.

    **Parameters:**
    - **user**: An object containing the user's name and city name.
    - **db**: Database session dependency.

    **Returns:**
    - A message indicating whether the user was created or updated.
    """
    return insert_user_data(db, user.name, user.city_name)