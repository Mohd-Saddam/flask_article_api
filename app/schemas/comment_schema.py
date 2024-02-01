from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import ma
from app.models.comment import Comment

class CommentSchema(SQLAlchemyAutoSchema):
    """
    Schema for serializing and deserializing Comment model data.

    Meta:
        model (Comment): Specifies the model to be serialized/deserialized.
    """
    
    class Meta:
        model = Comment