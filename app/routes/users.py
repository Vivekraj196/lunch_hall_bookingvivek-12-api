# APIRouter is used to create routes separately from main.py
from fastapi import APIRouter, Depends, HTTPException

# Session is used to communicate with PostgreSQL
from sqlalchemy.orm import Session

# Our database session function
from app.database import get_db

# Our User database model
from app.models import User

# Registration schema
from app.schemas import UserCreate, UserLogin

# Password hashing function
from app.auth import create_access_token, hash_password, verify_password


# Create a router for user-related APIs
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ---------------- REGISTER USER ----------------
@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Check whether this email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    # If email already exists, stop registration
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash the password before storing it
    hashed_password = hash_password(user.password)

    # Create a new User database object
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    # Add user to the database session
    db.add(new_user)

    # Save the user permanently in PostgreSQL
    db.commit()

    # Return a simple response
    return {
        "message": "User registered successfully"
    }
@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    # Find the user by email
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    # If email is not found in database
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not registered. Please register first."
        )

    # Check whether the entered password is correct
    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    # Create JWT token after successful login
    token = create_access_token({
        "user_id": existing_user.id
    })

    # Return token to the user
    return {
        "access_token": token,
        "token_type": "bearer"
    }