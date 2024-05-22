# main.py
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
from models import Base
from schemas import Address, AddressCreate, AddressUpdate
from crud import get_address, get_addresses, create_address, update_address, delete_address
from utils import calculate_distance

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses/", response_model=Address)
def create_address_endpoint(address: AddressCreate, db: Session = Depends(get_db)):
    return create_address(db=db, address=address)

@app.get("/addresses/", response_model=List[Address])
def read_addresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    addresses = get_addresses(db, skip=skip, limit=limit)
    return addresses

@app.get("/addresses/{address_id}", response_model=Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    db_address = get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{address_id}", response_model=Address)
def update_address_endpoint(address_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    db_address = update_address(db, address_id=address_id, address=address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.delete("/addresses/{address_id}", response_model=Address)
def delete_address_endpoint(address_id: int, db: Session = Depends(get_db)):
    db_address = delete_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.get("/addresses/nearby/", response_model=List[Address])
def get_nearby_addresses(
    latitude: float,
    longitude: float,
    distance_km: float,
    db: Session = Depends(get_db)
):
    addresses = get_addresses(db)
    nearby_addresses = [
        address for address in addresses
        if calculate_distance(latitude, longitude, address.latitude, address.longitude) <= distance_km
    ]
    return nearby_addresses
