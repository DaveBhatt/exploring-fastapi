from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) # This creates a foreign key relationship between the posts table and the users table, linking each post to a specific user (the owner of the post). The owner_id column in the posts table references the id column in the users table, and is set to not allow null values, ensuring that every post must be associated with a user.

    owner = relationship("User") # This sets up a relationship between the Post model and the User model, allowing us to easily access the user who owns a post through the owner attribute of a Post instance. For example, if we have a Post instance called post, we can access the email of the user who owns that post with post.owner.email.

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    phone_number = Column(String)
    
class Vote(Base):

    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True) # This creates a composite primary key using both the user_id and post_id columns. This means that each combination of user_id and post_id must be unique in the votes table, ensuring that a user can only vote once for a specific post.
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    

    