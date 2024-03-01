from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, database
from . import oauth2

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)   


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_post = vote_query.first()
    if vote.direction == 1:
        if found_post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already voted for this post")
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote successfully created"}
    else:
        if not found_post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have not voted for this post")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote successfully removed"}
