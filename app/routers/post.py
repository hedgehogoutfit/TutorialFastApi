from fastapi import HTTPException, status, Response, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(search: Optional[str] = "", db: Session = Depends(get_db),
              limit: int = 10):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()

    results = db.query(models.Post, func.count(
        models.Vote.post_id).label("votes_count")
                       ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)
    ).limit(limit).all()

    return results


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostStr, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s)
    # returning *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)

    new_post = models.Post(owner_id=current_user.id, title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts
    # where id = %s""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(
        models.Vote.post_id).label("votes_count")
                       ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""delete from posts where id = %s
    # returning *""", (id,))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostRes)
def update_post(id: int, post: schemas.PostStr, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s
    #  returning *""", (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_ = post_query.first()
    if not post_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()