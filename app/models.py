from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.orm import relationship


Base = declarative_base()


class ParentProfile(Base):
    __tablename__ = "parent_profiles"

    id = Column(String, primary_key=True, index=True)

    children = relationship(
        "Child", back_populates="parent", cascade="all, delete-orphan"
    )


class Child(Base):
    __tablename__ = "children"

    id = Column(String, primary_key=True, index=True, default=func.uuid_generate_v4())
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    avatar = Column(String, nullable=True)
    parent_id = Column(String, ForeignKey("parent_profiles.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    parent = relationship("ParentProfile", back_populates="children")
