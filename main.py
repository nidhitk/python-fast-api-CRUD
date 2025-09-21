from fastapi import FastAPI
from models import product
from database import Session,engine
import database_models

# product=product()
app=FastAPI()
database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    # print("welcome nidhi")
    return "welcome nidhi" 
products=[
    product(id=1,name="phone",description="budget phone",price=99,quantity=10),
    product(id=3,name="laptop",description="gaming laptop",price=978,quantity=6),
    product(id=5,name="pen",description="black pen",price=10,quantity=1),
    product(id=7,name="book",description="note book",price=30,quantity=5)
   
]
@app.get("/products")
def get_all_products():
    # db connection
    # query
    db=Session()
    db.query()
    return products

# @app.get(products/{id})
# def one_product(id=ids):
#     for product in products:
#         if product[id]==id:
#             return product
@app.get("/product")
def get_product_by_id(ids:int):
    for product in products:
        if product.id==ids:
           return product
    
    return "product not found"

@app.post("/product/")
def add_product(id:int,product:product):
    products.append(product)
    return {"product added":product}


@app.put("/product")
def update_product(product:product):
    for i in range(len(products)):
        if products[i].id==id:
            products[i]=product
            return {"product added succesfully":product}
        
    return "product not found"   
@app.delete("/product")  
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id==id:
            products.remove(products[i])
            return "product deleted"
    return "product not found"    


