from sqlalchemy import Column, BIGINT, VARCHAR, BLOB, TIMESTAMP

from database.database import Base


class User(Base):
    __table__name = "USERS"
    user_id = Column("USER_ID", BIGINT, primary_key=True, autoincrement=True)
    username = Column("USERNAME", VARCHAR)
    mail = Column("MAIL", VARCHAR, unique=True)
    password = Column("PASSWORD", VARCHAR)

    # construction_trees = relationship("ConstructionTree", back_populates="owner")


class ConstructionTree(Base):
    __table__name = "CONSTRUCTION_TREES"
    tree_id = Column("TREE_ID", BIGINT, primary_key=True, autoincrement=True)
    tree_data = Column("TREE_DATA", BLOB, unique=True)
    created_time = Column("CREATED_TIME", TIMESTAMP)
    # user_id = Column("USER_ID", BIGINT, ForeignKey("USERS.USER_ID"))

    # owner = relationship("User", back_populates="construction_trees")
