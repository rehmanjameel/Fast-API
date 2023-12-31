
import uvicorn
from fastapi import FastAPI
from mongo_fast.routes.route import router


app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("fast_mongo:app", host="0.0.0.0", port=8000, reload=True)

# from pymongo.mongo_client import MongoClient

# uri = "mongodb+srv://admin:test1234@cluster0.boymthh.mongodb.net/?retryWrites=true&w=majority"
#
# # Create a new client and connect to the server
# client = MongoClient(uri)
#
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
#
