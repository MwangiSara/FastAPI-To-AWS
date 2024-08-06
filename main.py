from fastapi import FastAPI,HTTPException
import random
import os
import json
from pydantic import BaseModel
from typing import Optional, Literal
from uuid import uuid4
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# creating a model of how our book will look like(entail) using pydantic
class BookModel(BaseModel):
    book_id: Optional[str] = uuid4().hex
    name:str
    price: float
    genre : Literal['fiction','Motivational','SciFi','Romance']

BOOKS_FILE = "books.json"
BOOK_DATABASE = []

#checking if we have our json file and then liading the books there
if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOK_DATABASE = json.load(f)

# /
@app.get("/")
async def home():
    return {"message":"Welcome to My Book Store"}
# /list-books
@app.get("/list-books")
async def list_books():
    return {"books":BOOK_DATABASE}
# /book-by-index/{index}
@app.get("/book-by-index/{index}")
async def book_by_index(index:int):
    if index < 0 or index >= len(BOOK_DATABASE):
        raise HTTPException(status_code=404, detail=f"index {index} out of range ({len(BOOK_DATABASE)}). ")
    else:
        return {"book":BOOK_DATABASE[index]}
# /get-random-book
@app.get("/get-random-book")
async def get_random_book():
    return random.choices(population=BOOK_DATABASE)

# /add-books
@app.post("/add-books")
async def add_books(book:BookModel):
    book.book_id= uuid4().hex #creating a random bookid everytime we add a book
    json_book = jsonable_encoder(book) #converting book to a json format
    BOOK_DATABASE.append(json_book) #adding book to bookdb
    #adding the book in my json db
    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOK_DATABASE, f)
    return  {"Message":f"book {book} successfuly added", "book_id":book.book_id}

# /get-book?id=...
@app.get("/get-book")
async def get_book(book_id):
    for book in BOOK_DATABASE:
        if book['book_id'] == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Not Found Book {book_id}. ")