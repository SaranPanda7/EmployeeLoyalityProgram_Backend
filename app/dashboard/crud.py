from datetime import datetime, timezone
from typing import Any
from fastapi import HTTPException
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import or_, select
from app.reward.models import *
from app.user.models import UserReward
from app.user.models import User
from app.user.schema import SchemaUser
from app.reward.schema import CreateRewardSchema
from app.dashboard.models import Banner, Images
from app.dashboard.schema import CreateSchemaBanner, UpdateSchemaBanner


def get_assigned_reward_count(db: Session):

    try:

        stmt = db.query(
            UserReward.reward_id,  func.count(
                UserReward.reward_id).label("count")
        ).group_by(UserReward.reward_id).subquery()

        return [dict(id=u.id, title=u.title, count=0 if count is None else count) for u, count in db.query(Reward, stmt.c.count).outerjoin(stmt, Reward.id == stmt.c.reward_id).order_by(Reward.title).all()]

    except SQLAlchemyError as e:
        return None


def get_banner_from_db(db: Session):

    try:

        return db.query(Banner).filter(Banner.is_deleted == False).all()
    except SQLAlchemyError as e:
        return None


def get_all_images(db: Session):

    try:
        return db.query(Images).filter(Images.is_deleted == False).all()

    except SQLAlchemyError as e:
        return None


def create_banner(db: Session, banner: CreateSchemaBanner):
    try:
        db_banner = Banner(
            title=banner.title,
            image=banner.image,
            start_date=banner.start_date,
            end_date=banner.end_date
        )

        db.add(db_banner)
        db.commit()
        db.refresh(db_banner)

        return db_banner

    except SQLAlchemyError as e:
        return None


def delete_banner(title: str, db: Session) -> Any:
    """Delete Banner"""
    try:
        db_banner = db.query(Banner).filter(
            Banner.title == Banner.title).first()

        db_banner.is_deleted = True
        db_banner.deleted_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_banner)

        return True

    except SQLAlchemyError as e:
        return None


def update_banner(title: str, db: Session, banner: UpdateSchemaBanner) -> Any:
    """Update A Banner"""
    try:

        db_banner = db.query(Banner).filter(
            title == title).first()

        db_banner.title = banner.title
        db_banner.image = banner.image
        db_banner. is_updated = True
        db_banner.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(db_banner)

        return True

    except SQLAlchemyError as e:
        return True


def get_top_performer_count_from_db(db: Session):

    try:

        stmt = db.query(
            User.first_name,  func.count(
                Reward.points).label("count")
        ).group_by(User.first_name).order_by(sum(Reward.points)).subquery()

        return [dict(User.first_name, Reward.points, count=0 if count is None else count) for r, count in db.query(Reward, stmt.c.count).outerjoin(stmt, Reward.id == stmt.c.id).order_by(Reward.points).all()]

    except SQLAlchemyError as e:
        return None
