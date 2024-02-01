
from datetime import datetime
from app import db
import pytz 
indian_timezone = pytz.timezone('Asia/Kolkata')  # 'Asia/Kolkata' for Indian Standard Time


class Article(db.Model):
    """
    Model class for Article, representing articles in the application.
    Attributes:
        id (int): Primary key for the article.
        title (str): Title of the article.
        content (str): Content of the article.
        author (str): Author of the article.
        is_published (bool): Flag indicating if the article is published (default is True).
        pub_date (datetime): Published date of the article (default is the current date in Indian Standard Time).
        comments (relationship): Relationship with Comment model, establishing a backref for easy access to comments.
        created_at (datetime): Timestamp for the creation date of the article.
        updated_at (datetime): Timestamp for the last update of the article.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_published = db.Column(db.Boolean, default=True) # I'm using by default published
    pub_date = db.Column(db.DateTime, default=lambda: datetime.now(indian_timezone)) # I'm using by default published date
    comments = db.relationship('Comment', backref='article', lazy=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(indian_timezone))
    updated_at = db.Column(db.DateTime,onupdate=lambda: datetime.now(indian_timezone))


    def __repr__(self):
        """
        Return a string representation of the Article object.
        """
        return f"<Article {self.title}>"