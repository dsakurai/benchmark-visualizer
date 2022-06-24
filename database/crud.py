import datetime

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_id(db: Session, user_id: int) -> Session.query:
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_mail(db: Session, mail: str) -> Session.query:
    return db.query(models.User).filter(models.User.mail == mail).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Session.query:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    password = get_password_hash(user.password)
    db_user = models.User(mail=user.mail, username=user.username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_construction_tree(
    db: Session, construction_tree: schemas.ConstructionTree
) -> models.ConstructionTree:
    db_construction_tree = models.ConstructionTree(
        tree_data=construction_tree.tree_data, created_time=datetime.datetime.now()
    )
    db.add(db_construction_tree)
    db.commit()
    db.refresh(db_construction_tree)
    return db_construction_tree
