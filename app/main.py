from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import post, user, auth, vote
from .config import settings

# Base.metadata.create_all(bind=engine) # This creates the tables in the database based on the SQLAlchemy models defined in models.py. It checks if the tables already exist and only creates them if they don't, preventing errors from trying to create tables that already exist.

app = FastAPI()

origins = ["*"] # This is a list of allowed origins for cross-origin requests. You can specify the domains that are allowed to access your API from a different origin (e.g., your frontend application running on localhost:3000). This helps to prevent unauthorized access to your API from untrusted sources.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True, # This allows cookies and other credentials to be included in cross-origin requests. This is necessary if your frontend application needs to send authentication tokens or other sensitive information in the request.
    allow_methods=["*"], # This allows all HTTP methods (GET, POST, PUT, DELETE, etc.) in cross-origin requests. You can specify specific methods if you want to restrict the allowed methods for security reasons.
    allow_headers=["*"], # This allows all headers in cross-origin requests. You can specify specific headers if you want to restrict the allowed headers for security reasons.

)

app.include_router(post.router) # This includes the post router in the main application, allowing us to define all the routes related to posts in a separate file (routers/post.py) and keep our code organized.
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application! This is the root endpoint."}





