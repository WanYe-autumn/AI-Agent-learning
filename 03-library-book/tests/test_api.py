from fastapi.testclient import TestClient
from app import app
from models import Book
from database import init_db,add_book_to_db,borrow_book_from_db
import pytest

@pytest.fixture
def test_db(tmp_path,monkeypatch):
    db_path = tmp_path / "test.db"

    init_db(db_path)

    monkeypatch.setattr("app.DB_PATH", str(db_path))

    return db_path

@pytest.fixture
def client(test_db):
    with TestClient(app) as test_client:
        yield test_client

def test_books(client):
    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == []

def test_get_books_by_id_a(test_db,client):
    book = Book(title="haha",author="zuojia1",price=30,borrowed=True)
    add_book_to_db(book, test_db)
    response = client.get("/books/1")
    
    assert response.status_code == 200
    assert response.json() == {
        "title": "haha",
        "author": "zuojia1",
        "price": 30.0,
        "borrowed": True
    }

def test_get_book_not_found(test_db,client):
    response = client.get("/books/999")

    assert response.status_code == 404

def test_query_parameter_true(test_db,client):
    book = Book(title="haha",author="zuojia1",price=30,borrowed=True)
    add_book_to_db(book, test_db)
    response = client.get("/books?borrowed=true")

    assert response.status_code == 200
    assert response.json() == [{
        "title": "haha",
        "author": "zuojia1",
        "price": 30.0,
        "borrowed": True
    }]

def test_query_parameter_false(test_db,client):
    book = Book(title="haha",author="zuojia1",price=30,borrowed=False)
    add_book_to_db(book, test_db)
    response = client.get("/books?borrowed=false")

    assert response.status_code == 200
    assert response.json() == [{
        "title": "haha",
        "author": "zuojia1",
        "price": 30.0,
        "borrowed": False
    }]

def test_post_create_book(test_db,client):
    response = client.post(
    "/books",
    json={
        "title": "Python",
        "author": "A",
        "price": 88
    }
)
    assert response.status_code == 200
    assert response.json() == {
    "title": "Python",
    "author": "A",
    "price": 88.0,
    "borrowed": False
}
    get_response = client.get("/books")
    assert get_response.json() ==  [
    {
        "title": "Python",
        "author": "A",
        "price": 88.0,
        "borrowed": False
    }
]

def test_post_create_book_yichang1(test_db,client):
    response = client.post(
        "/books",
        json={
            "title": "Python",
            "author": "B",
        }
    )
    assert response.status_code == 422

def test_post_create_book_yichang2(test_db,client):
    response = client.post(
        "/books",
        json={
            "title": "Python",
            "author": "B",
            "price": -1
        }
    )
    assert response.status_code == 422

def test_post_create_book_yichang3(test_db,client):
    book = Book(title="haha",author="zuojia1",price=30,borrowed=False)
    add_book_to_db(book, test_db)
    response = client.post(
        "/books",
        json={
            "title": "haha",
            "author": "zuojia1",
            "price": 30
        }
    )
    assert response.status_code == 409

def test_patch_update_book(test_db,client):
    book = Book(title="haha",author="zuojia1",price=30,borrowed=False)
    add_book_to_db(book, test_db)
    response = client.patch(
        "/books/1",
        json={
            "title": "djh"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "book_id": 1,
        "update": {
        "title": "djh"
        }
    }
    get_response = client.get("/books/1")

    assert get_response.json() == {
        "title": "djh",
        "author": "zuojia1",
        "price": 30,
        "borrowed": False
    }

def test_delete_book(test_db,client):
    book = Book(title="hahaha", author="djh", price=30, borrowed=True)
    add_book_to_db(book, test_db)
    response = client.delete(
        "books/1",
    )
    assert response.status_code == 200
    get_response = client.get("/books/1")
    assert get_response.status_code == 404

def test_delete_book_404(test_db,client):
    response = client.delete("/books/999")
    assert response.status_code == 404

def test_patch_price_200(test_db,client):
    book=Book(title="niulai", author="djh", price="77.0", borrowed=False)
    add_book_to_db(book,test_db)
    response = client.patch(
        "/books/1/price",
        json={"price":666})
    
    assert response.status_code == 200
    get_response = client.get("/books/1")
    assert get_response.status_code == 200
    assert get_response.json()["price"] == 666

@pytest.mark.parametrize("invalid_price",[0,-1])
def test_patch_price_422(client,test_db,invalid_price):
    response = client.patch(
        "/books/1/price",
        json={"price": invalid_price}
    )

    assert response.status_code == 422

def test_patch_price_404(client,test_db):
    response = client.patch(
        "/books/999/price",
        json={"price":600})
    
    assert response.status_code == 404

def test_patch_price_409(test_db,client):
    book=Book(title="niulai", author="djh", price="77.0", borrowed=True)
    add_book_to_db(book,test_db)
    response = client.patch(
        "/books/1/price",
        json={"price":600})
    
    assert response.status_code == 409