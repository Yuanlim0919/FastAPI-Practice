import motor.motor_tornado 

Mongo_details = "mongodb://localhost:27017/"
client = motor.motor_tornado.MotorClient(Mongo_details)
db = client.books
user_collection = db.get_collection('userinfo')
book_collection = db.get_collection('book_collections')