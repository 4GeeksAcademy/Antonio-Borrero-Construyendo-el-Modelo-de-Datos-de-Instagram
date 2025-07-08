from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    profile: Mapped["Profile"] = relationship(back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Profile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="profile")

    posts: Mapped[List["Post"]] = relationship(back_populates="profile")

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(String(200), nullable=True)

    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    profile: Mapped["Profile"] = relationship(back_populates="posts")

    hashtags: Mapped[List["Hashtag"]] = relationship(secondary="post_hashtag", back_populates="posts")

class Hashtag(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(30), nullable=True)

    posts: Mapped[List["Post"]] = relationship(secondary="post_hashtag", back_populates="hashtags")

post_hashtag = Table(
    "post_hashtag",
    db.metadata,
    Column("post_id", ForeignKey("post.id")),
    Column("hashtag_id", ForeignKey("hashtag.id"))
)