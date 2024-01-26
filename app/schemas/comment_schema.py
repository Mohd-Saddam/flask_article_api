from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import ma
from app.models.comment import Comment

class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment