from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import pyd_models
import db_models
from db_config import SessionLocal, engine
from sqlalchemy.orm import Session

"""
Configuration Setup 
"""
# FastAPI instance
app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware, allow_origins="http://localhost:3000", allow_methods=["*"]
)

# Create the database tables
db_models.Base.metadata.create_all(bind=engine)

# DB connection function
def db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Populate the database with initial data
"""

products = [
    pyd_models.Product(
        id=1,
        name="Product 1",
        price=19.99,
        description="This is product 1",
        quantity=10,
    ),
    pyd_models.Product(
        id=2, name="Product 2", price=29.99, description="This is product 2", quantity=5
    ),
    pyd_models.Product(
        id=3, name="Product 3", price=39.99, description="This is product 3", quantity=0
    ),
    pyd_models.Product(
        id=4,
        name="Product 4",
        price=49.99,
        description="This is product 4",
        quantity=20,
    ),
    pyd_models.Product(
        id=5,
        name="Product 5",
        price=59.99,
        description="This is product 5",
        quantity=15,
    ),
]


def init_db():
    db = SessionLocal()
    count = db.query(db_models.Product).count
    if count == 0:
        for product in products:
            db.add(db_models.Product(**product.model_dump()))
        db.commit()


init_db()

"""
APIs
"""


@app.get("/")
def greet():
    return f"""API to manage products."""


@app.get("/products")
def read_products(db: Session = Depends(db_connection)):
    db_products = db.query(db_models.Product).all()
    return db_products


@app.get("/products/{id}")
def read_product(id: int, db: Session = Depends(db_connection)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        return db_product
    else:
        return "Product not found"


@app.post("/products")
def add_product(product: pyd_models.Product, db: Session = Depends(db_connection)):
    db.add(db_models.Product(**product.model_dump()))
    db.commit()
    return "Product added successfully!"


@app.put("/products/{id}")
def update_product(
    id: int, updated_product: pyd_models.Product, db: Session = Depends(db_connection)
):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.price = updated_product.price
        db_product.description = updated_product.description
        db_product.quantity = updated_product.quantity
        db.commit()
        return "Product Updated successfully!"
    else:
        return "Product not found"


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(db_connection)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted successfully!"
    else:
        return "Product not found"
