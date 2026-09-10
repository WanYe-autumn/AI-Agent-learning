from fastapi import FastAPI,HTTPException
from models import Book
from database import get_book_from_db,get_book_by_id,whether_borrowed_book_in_db,add_book_to_db,update_book_in_db,delete_book_from_db,whether_book_in_db,update_price_by_book_id
from pydantic import BaseModel, Field

DB_PATH = "library.db"
app = FastAPI()

class BookCreate(BaseModel):
    title: str
    author: str
    price: float = Field(gt=0)
    borrowed: bool = False

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    price: float | None = Field(default=None, gt=0)
    borrowed: bool | None = None
    
@app.post("/books")
def create_book(book: BookCreate):
    exists = whether_book_in_db(book.title, book.author ,DB_PATH)

    if exists:
        raise HTTPException(
            status_code=409,
            detail="Book already exists"
        )
    new_book = Book(
        title=book.title,
        author=book.author,
        price=book.price,
        borrowed=book.borrowed
    )
    add_book_to_db(new_book ,DB_PATH)
    return new_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    result = delete_book_from_db(book_id, DB_PATH)
    if result is False:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return result

@app.patch("/books/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    update_data = book_update.model_dump(exclude_unset=True)
    update_book_in_db(book_id, update_data, DB_PATH)
    return{
        "book_id": book_id,
        "update": update_data
    }

@app.get("/books/{book_id}")
def get_books_by_id_a(book_id: int):
    result = get_book_by_id(book_id, DB_PATH)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return result

@app.get("/books")
def get_books(borrowed: bool | None = None):                                                        #query parameter
    if borrowed is None:
        all_books = get_book_from_db(DB_PATH)
        return all_books
              
    books = whether_borrowed_book_in_db(borrowed, DB_PATH)
    return books

@app.patch("/books/{book_id}/price")
def update_book_price(book_id:int, book_update: BookUpdate):
    result = get_book_by_id(book_id, DB_PATH)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="书本不存在"
        )
    borrowed = result.borrowed
    if borrowed:
        raise HTTPException(
            status_code=409,
            detail="禁止修改，书本已经借出"
        )
    if not borrowed:
        update_data = book_update.price
        update_price_by_book_id(book_id, update_data, DB_PATH)
        return get_book_by_id(book_id,DB_PATH)
   
