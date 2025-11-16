from fastapi import Depends,FastAPI
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session


# product=product()
app=FastAPI()
database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    # print("welcome nidhi")
    return "welcome nidhi" 
products=[
    Product(id=1,name="phone",description="budget phone",price=99,quantity=10),
    Product(id=3,name="laptop",description="gaming laptop",price=978,quantity=6),
    Product(id=5,name="pen",description="black pen",price=10,quantity=1),
    Product(id=7,name="book",description="note book",price=30,quantity=5)
   
]


def get_db():
    db=session()
    try:
        yield db
    finally:   
        db.close()

def init_db():
    db=session()
    count=db.query(database_models.Product).count
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()  

     
init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    # db connection
    # query
    db_products=db.query(database_models.Product).all()
    return db_products

# @app.get(products/{id})
# def one_product(id=ids):
#     for product in products:
#         if product[id]==id:
#             return product
@app.get("/product/{id}")
def get_product_by_id(id:int,db: Session = Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    return "product not found"
    

@app.post("/product/")
def add_product(product:Product,db: Session = Depends(get_db)):
    db_product=database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"product added succesfully":db_product}



@app.put("/product")
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name=product.name    
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "product updated"
    
    return "product not found"  


@app.delete("/product")  
def delete_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted"
    return "product not found"


