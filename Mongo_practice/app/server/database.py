from re import L
import motor.motor_tornado 
from bson.objectid import ObjectId
from fastapi import HTTPException,Header
import urllib.parse
import pymongo.errors
from server.db_init import book_collection

# 由於MongoDB 的 Async 

def CreateUser():
    global user_collection
    Mongo_details = "mongodb://localhost:27017/"
    client = motor.motor_tornado.MotorClient(Mongo_details)
    db = client.books
    user_collection = db.get_collection('userinfo')
    return user_collection

async def UserVerify(user:str = Header(...,min_length=1,max_length=99),
                pwd:str = Header(...,min_length=8,max_length=99)):

    global database, book_collection
    try:
        Mongo_details = f"mongodb://{user}:{urllib.parse.quote_plus(pwd)}@localhost:27017/books"
        client = motor.motor_tornado.MotorClient(Mongo_details)
        database = client.books
        await database.command("collstats","book_collections")
        book_collection = database.get_collection("book_collections")        

        #開始有Authentication fail 的error message
    except pymongo.errors.OperationFailure:
        raise HTTPException(400,"Authentication Failed!")

def book_helper(book) -> dict:
    return {
        "title":book["title"],
        "author":book["author"],
        "year_published":book["year_published"]
    }

#retreive all books in DB
async def retreive_boks():
    books = []
    async for book in book_collection.find():
        books.append(book_helper(book))
    return books

#add book to DB
async def add_book(book_data)-> dict:
    try:
        book = await book_collection.insert_one(book_data)
        new_book = await book_collection.find_one({"_id":book.inserted_id})
        return book_helper(new_book)
    except pymongo.errors.OperationFailure:
        raise HTTPException(400,"Unsuccessful post!")
    
#Retreive book with matching idimage.png
async def retreive_book(id:str) -> dict:
    book = await book_collection.find_one({"_id":ObjectId(id)})
    if book:
        return book_helper(book)

#Update book with matching id
async def update_book(id:str,data:dict):
    if len(data)<1:
        return False
    book = await book_collection.find_one({"_id":ObjectId(id)})
    if book:
        updated_book = await book_collection.update_one(
            {"_id":ObjectId(id)},{"$set":data})
        if updated_book:
            return True
        return False

async def delete_book(id:str):
    book = await book_collection.find_one({"_id":ObjectId(id)})
    if book:
        await book_collection.delete_one({"_id":ObjectId(id)})
        return True