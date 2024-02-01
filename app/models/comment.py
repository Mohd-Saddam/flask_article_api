from datetime import datetime
from app import db
import pytz 
indian_timezone = pytz.timezone('Asia/Kolkata')  # 'Asia/Kolkata' for Indian Standard Time


class Comment(db.Model):
    """
    Model class for Comment, representing comments on articles in the application.
    Attributes:
        id (int): Primary key for the comment.
        author (str): Author of the comment.
        content (str): Content of the comment.
        article_id (int): Foreign key referencing the associated article's id.
        created_at (datetime): Timestamp for the creation date of the comment.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(indian_timezone))

    def __repr__(self):
        """
        Return a string representation of the Comment object.
        """
        return f"<Comment {self.id}>"