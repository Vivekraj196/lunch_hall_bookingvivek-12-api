from fastapi import APIRouter, Depends

# Database session
from sqlalchemy.orm import Session

# Database dependency
from app.database import get_db

# Seat database model
from app.models import Seat


# Create seats router
router = APIRouter(
    prefix="/seats",
    tags=["Seats"]
)


# Get all seats
@router.get("/")
def get_seats(
    db: Session = Depends(get_db)
):
    # Get all seats from PostgreSQL
    seats = db.query(Seat).all()

    # Return the seats
    return seats