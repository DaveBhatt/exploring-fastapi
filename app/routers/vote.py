from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2



router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first() # This checks if the post that the user is trying to vote on exists in the database. If the post does not exist, it will return None, which can be used to raise an HTTPException indicating that the post was not found.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist!")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) # This creates a query object that filters the votes based on the provided post_id and the user_id of the current user. This is used to check if the user has already voted for the specified post.
    found_vote = vote_query.first() # This executes the query and retrieves the first result, which should be the vote if it exists. If no vote is found, it will return None.

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id) # This creates a new Vote object with the specified post_id and user_id, which represents a new vote by the user for the specified post.
        db.add(new_vote)
        db.commit() # Commit the transaction to add the new vote to the database
        return {"message": "Successfully added vote!"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist!")
        
        vote_query.delete(synchronize_session=False) # This deletes the existing vote from the database, effectively removing the user's vote for the specified post.
        db.commit() # Commit the transaction to delete the vote from the database
        return {"message": "Successfully deleted vote!"}
