from fastapi import APIRouter, Body, Depends, HTTPException, Header
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth import exceptions
from server.database import(
    add_book,
    delete_book,
    retreive_boks,
    retreive_book,
    update_book,
    UserVerify
)

from server.models.books import (
    ErrorResponseModel,
    ResponseModel,
    BookSchema,
    UpdateBookModel,
)
'''
async def UserVerify(
    username: str = Header(...,min_length=1,max_length=99),
    password: str = Header(...,min_length=8,max_length=99)
):
    if username != UserInfo.username:
        raise HTTPException(400,"User not found!")
    if password != UserInfo.password:
        raise HTTPException(400,"Invalid password!")
'''
router = APIRouter()
@router.post("/",response_description="Book data added!")#要記得補回dependency
async def add_book_data(book:BookSchema=Body(...),Authorize : AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except exceptions.MissingTokenError:
        raise HTTPException(401,"Unauthorized!")
    book = jsonable_encoder(book)
    new_book = await add_book(book)
    return ResponseModel(new_book,"Book added successfully!")

@router.get("/",response_description="Books Retrieved")
async def get_books():
    books = await retreive_boks()
    if books:
        return ResponseModel(books,"Books Retrieved Successfully")
    return ResponseModel(books,"No book data")

@router.get("/{id}",response_description="Book details retreived")
async def get_book_data(id):
    book = await retreive_book(id)
    if book:
        return ResponseModel(book,"Book details retreived.")
    return ResponseModel("Error:",404,"Book doesn't exist")

@router.put("/{id}")
async def update_book_data(id:str,req:UpdateBookModel=Body(...)):
    req = {k:v for k, v in req.dict().items() if v is not None}
    updated_book = await update_book(id,req)
    if updated_book:
        return(ResponseModel("Book with id: {} is successfully updated".format(id),
        "Details updated"))
    return(ResponseModel("Error:",400,"Book is not updated successfully, please check syntax"))

@router.delete("/{id}",response_description="Book deleted from database")
async def delete_book_data(id:str):
    deleted_book = await delete_book(id)
    if deleted_book:
        return ResponseModel(
            "Book with id {} removed".format(id), "Book removed successfully"
        )
    return ResponseModel(
        "Error",404,"Book dosen't exist"
    )