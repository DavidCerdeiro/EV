from requests import Session
from app.models.user import User



def insert_user_data(db: Session, name: str, city_name: str):
    """
    Inserts or updates user data in the database.

    **Parameters:**
    - **db**: Database session dependency.
    - **name**: The name of the user.
    - **city_name**: The name of the user's city.

    **Returns:**
    - A message indicating whether the user was created or updated.
    """
    existing_user = db.query(User).first()
    
    if existing_user:
        if existing_user.name == name:
            # If the user only has changed the city name, update it
            existing_user.city_name = city_name
            db.commit()
            return {"message": f"User '{name}' updated successfully."}
        else:
            # Otherwise, delete the existing user and create a new one
            db.delete(existing_user)
            
    new_user = User(
        name=name,
        city_name=city_name,
    )
    db.add(new_user)
    db.commit()

    return {"message": f"User '{name}' created successfully."}