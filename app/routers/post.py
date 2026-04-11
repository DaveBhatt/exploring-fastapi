from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from sqlalchemy import func

from .. import oauth2
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])

def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 15, skip: int = 0, search: Optional[str] = ""):

    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # This queries the database for all posts that have an owner_id matching the ID of the current user. This ensures that users can only see their own posts and not the posts of other users. The results are returned as a list of Post objects, which are then serialized to JSON and sent back to the client as the response to the GET request.
    # %20 is the URL-encoded representation of a space character, so this query will filter posts based on whether their title contains the search string provided in the query parameters. The limit and skip parameters are used for pagination, allowing clients to specify how many posts to return and how many posts to skip before starting to return results.
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # This query retrieves posts along with the count of votes for each post. It performs a left outer join between the Post and Vote tables, grouping the results by post ID to get the total number of votes for each post. The filter, limit, and offset parameters are applied to allow for searching and pagination of the results. The resulting list contains tuples of Post objects and their corresponding vote counts, which are then serialized to JSON and sent back to the client as the response to the GET request.

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post_dict = post.model_dump()   # Use model_dump instead of deprecated dict method to convert the Pydantic model to a dictionary.
    # post_dict['id'] = randrange(0, 1000000) # Generate a random ID for the post
    # my_posts.append(post_dict)   
    # return {"data": post_dict}
    
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() # Commit the transaction to save the new post to the database

    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) # Use model_dump instead of deprecated dict method to convert the Pydantic model to a dictionary, and unpack the dictionary into the Post model constructor. Also, set the owner_id field to the ID of the current user, which is obtained from the get_current_user dependency.
    db.add(new_post)
    db.commit() # Commit the transaction to save the new post to the database
    db.refresh(new_post) # Refresh the instance to get the generated ID and other fields from the database
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() # This query retrieves a single post along with the count of votes for that post. It performs a left outer join between the Post and Vote tables, grouping the results by post ID to get the total number of votes for the specified post. The filter is applied to retrieve only the post with the given ID. The resulting tuple contains a Post object and its corresponding vote count, which is then serialized to JSON and sent back to the client as the response to the GET request.

    # post = db.query(models.Post).filter(models.Post.id == id).first() # This queries the database for a single post with the specified ID. It returns the first result that matches the filter condition, which should be the post with the given ID. If no post is found, it will return None. This allows us to retrieve a specific post based on its unique identifier and return it as the response to the GET request.

    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()
    # post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found!")
    # if post.owner_id != current_user.id: # Check if the owner of the post matches the current user
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id) # This creates a query object that filters the posts based on the provided ID. The query object allows us to perform operations like delete or update on the filtered results.
    post = post_query.first() # This executes the query and retrieves the first result, which should be the post with the specified ID. If no post is found, it will return None.
    
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit() # Commit the transaction to delete the post from the database

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    
    if post.owner_id != current_user.id: # Check if the owner of the post matches the current user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit() # Commit the transaction to delete the post from the database
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # cursor.execute("UPDATE posts SET title =%s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                 (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit() # Commit the transaction to update the post in the database
    
    # index = find_index_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist!")
    
    if post.owner_id != current_user.id: # Check if the owner of the post matches the current user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit() # Commit the transaction to update the post in the database

    # post_dict = post.model_dump()
    # post_dict["id"] = id
    # my_posts[index] = post_dict

    return post_query.first()