from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Booking, Seat
from app.schemas import BookingCreate,BookingResponse
from app.auth import get_current_user


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


# Create a new booking
@router.post("/")
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    # Check whether the seat exists
    seat = db.query(Seat).filter(
        Seat.id == booking.seat_id
    ).first()

    if not seat:
        raise HTTPException(
            status_code=404,
            detail="Seat not found"
        )

    # Check whether this seat is already booked
    # for the requested time
    existing_booking = db.query(Booking).filter(
        Booking.seat_id == booking.seat_id,
        Booking.booking_time == booking.booking_time
    ).first()

    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="Seat already booked for this time"
        )

    # Create booking for the logged-in user
    new_booking = Booking(
        user_id=current_user_id,
        seat_id=booking.seat_id,
        booking_time=booking.booking_time
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {
        "message": "Seat booked successfully",
        "booking_id": new_booking.id
    }
@router.get("/my-bookings",response_model=list[BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user_id
    ).all()

    return bookings
# Cancel a booking
@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    # Find the booking
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user_id
    ).first()

    # Booking not found or does not belong to this user
    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Delete the booking
    db.delete(booking)
    db.commit()

    return {
        "message": "Booking cancelled successfully"
    }