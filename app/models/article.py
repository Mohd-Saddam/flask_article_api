
from datetime import datetime
from app import db
import pytz 
indian_timezone = pytz.timezone('Asia/Kolkata')  # 'Asia/Kolkata' for Indian Standard Time


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_published = db.Column(db.Boolean, default=True) # I'm using by default published
    pub_date = db.Column(db.DateTime, default=lambda: datetime.now(indian_timezone)) # I'm using by default published date
    comments = db.relationship('Comment', backref='article', lazy=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(indian_timezone))
    updated_at = db.Column(db.DateTime,onupdate=lambda: datetime.now(indian_timezone))


