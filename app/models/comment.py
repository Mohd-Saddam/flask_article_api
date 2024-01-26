from datetime import datetime
from app import db
import pytz 
indian_timezone = pytz.timezone('Asia/Kolkata')  # 'Asia/Kolkata' for Indian Standard Time


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(indian_timezone))