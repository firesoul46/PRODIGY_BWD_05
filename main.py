from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import date
from jose import jwt, JWTError
from sqlalchemy.orm import Session, joinedload  # Add joinedload here

import models, schemas, auth, database

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="Hotel Booking API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None: raise HTTPException(status_code=401)
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def home():
    return {"status": "Backend is online!"}

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_pwd = auth.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    return {"message": "User registered"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": auth.create_access_token({"sub": user.email}), "token_type": "bearer"}

@app.post("/rooms", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    new_room = models.Room(**room.model_dump(), owner_id=current_user.id)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@app.get("/rooms/search")
def search_rooms(check_in: date, check_out: date, city: str = None, db: Session = Depends(database.get_db)):
    booked_rooms = db.query(models.Booking.room_id).filter(
        models.Booking.check_in < check_out, 
        models.Booking.check_out > check_in
    ).subquery()
    
    query = db.query(models.Room).filter(models.Room.id.not_in(booked_rooms))
    if city: query = query.filter(models.Room.city == city)
    return query.all()

@app.post("/bookings")
def book_room(booking: schemas.BookingCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    overlap = db.query(models.Booking).filter(
        models.Booking.room_id == booking.room_id,
        models.Booking.check_in < booking.check_out,
        models.Booking.check_out > booking.check_in
    ).first()
    if overlap: raise HTTPException(status_code=400, detail="Room occupied")
    new_booking = models.Booking(**booking.model_dump(), user_id=current_user.id)
    db.add(new_booking)
    db.commit()
    return {"message": "Booking confirmed"}
@app.get("/my-bookings")
def get_my_bookings(
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # This query "joins" the Room table so we can see the hotel details
    bookings = db.query(models.Booking).options(
        joinedload(models.Booking.room)
    ).filter(models.Booking.user_id == current_user.id).all()
    
    if not bookings:
        return {"message": "You have no bookings yet."}
        
    # We format the data to make it easy for a frontend to read
    results = []
    for b in bookings:
        results.append({
            "booking_id": b.id,
            "hotel_name": b.room.title,
            "city": b.room.city,
            "check_in": b.check_in,
            "check_out": b.check_out,
            "price_per_night": b.room.price
        })
        
    return results

@app.post("/reviews")
def leave_review(
    review: schemas.ReviewCreate, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
    new_review = models.Review(**review.model_dump(), user_id=current_user.id)
    db.add(new_review)
    db.commit()
    return {"message": "Review submitted! Thank you."}