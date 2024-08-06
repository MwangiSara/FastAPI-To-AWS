from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#create a new app
app = FastAPI()

# creating an class using BaseModel( it is used for data validation and data conversion, helping you define data models and ensure data conforms to the expected format.)
class ItemClass(BaseModel):
    text:str = None # to make it required remove the defaule value, eg text:str
    is_done:bool = False
    

#define a path
@app.get("/")
def root():
    return {"message": "Hello, World!"}
# to run use uvicorn command: uvicorn filename:appName --reload. eg, uvicorn main:app --reload

#lets create different routes

items = []
# @app.post("/items")
# def create_item(item:int):
#     items.append(item)
#     return items
#to test this using curl command: curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:8080/items?item=apple"

#when using pydantic
@app.post("/items")
def create_item(item:ItemClass): #passinng the class ItemClass
    items.append(item)
    return items
#to test this using curl command: curl -X POST -H 'Content-Type: application/json' -d '{"text":"apple"}' 'http://127.0.0.1:8080/items'


#viewing a specific item on the list
# @app.get("/items/{item_id}")
# def get_item(item_id:int) -> str:
#     # item = items[item_id]
#     # return item
#     # lets add an error handler
#     if item_id < len(items):
#         return items[item_id]
#     else:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} Not Found")
# to test it using curl command: curl -X GET http://127.0.0.1:8000/items/0
    
#when using pydantic
@app.get("/items/{item_id}",response_model=ItemClass)
def get_item(item_id:int) -> ItemClass:  #passinng the class ItemClass
    # item = items[item_id]
    # return item
    # lets add an error handler
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} Not Found")
# to test it using curl command: curl -X GET http://127.0.0.1:8000/items/0


#using a query parameter
# @app.get("/items")
# def list_items(limit: int = 10):
#     return items[0:limit]
# to test it using curl command: curl -X GET http://127.0.0.1:8000/items?limit=3

# adding a response model: Response modeling overall procedure consists of several steps such as data preprocessing, feature construction, feature selection, class balancing, classification, and model evaluation; different data mining techniques and algorithms have been used for implementing each step of modeling.
@app.get("/items", response_model=list[ItemClass]) #so now we are telling the server and interfaces that response this route will be conforming to the ItemClass class 
def list_items(limit: int = 10):
    return items[0:limit]
# to test it using curl command: curl -X GET http://127.0.0.1:8000/items?limit=3