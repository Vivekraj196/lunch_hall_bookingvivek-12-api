# FastAPI framework
from fastapi import FastAPI

# Database Base and engine
from app.database import Base, engine

# Import models so SQLAlchemy knows our tables
from app import models

# Import our API routers
from app.routes import users, seats, bookings
from app.models import Seat
from app.database import SessionLocal


# Create FastAPI application
app = FastAPI(
    title="Lunch Hall Booking API"
)


# Create database tables in PostgreSQL
Base.metadata.create_all(bind=engine)


# Connect Users routes
app.include_router(users.router)

# Connect Seats routes
app.include_router(seats.router)
# Connect Bookings routes
app.include_router(bookings.router)



# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Lunch Hall Booking API is running"
    }
db = SessionLocal()

if db.query(Seat).count() == 0:
    for number in range(1, 11):
        db.add(Seat(seat_number=number))

    db.commit()

db.close()