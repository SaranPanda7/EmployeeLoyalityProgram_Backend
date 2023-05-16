from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.sample.models import Student


def get_user_from_ad(db: Session):

    _ = db.query(Student).all()

    if _ is None:
        raise HTTPException(status_code=404, detail="User not found")
    return _

