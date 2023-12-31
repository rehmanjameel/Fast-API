import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID

from fast_alchemy import models
from fast_alchemy.database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)


BOOKS = []


@app.get("/get_books")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()
    # return BOOKS


@app.post("/add_book")
def create_book(book: Book, db: Session = Depends(get_db)):
    # BOOKS.append(book)

    # adding/saving book data in db
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book


@app.put("/update_book/{book_id}")
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):

    # simple without db
    # counter = 0
    #
    # for x in BOOKS:
    #     counter += 1
    #     if x.id == book_id:
    #         BOOKS[counter - 1] = book
    #         return BOOKS[counter - 1]

    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()  # first mean returns only
    # filtered result

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id}: Does not exist")

    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book


@app.delete("/delete_book/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # counter = 0
    # for x in BOOKS:
    #     counter += 1
    #     if x.id == book_id:
    #         del BOOKS[counter - 1]
    #         return f"ID: {book_id} deleted"

    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID: {book_id} : Does not exist"
        )

    db.query(models.Books).filter(models.Books.id == book_id).delete()
    db.commit()


if __name__ == "__main__":
    uvicorn.run("books:app", host="0.0.0.0", port=8000, reload=True)
