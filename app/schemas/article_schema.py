
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import ma
from app.models.article import Article

class ArticleSchema(SQLAlchemyAutoSchema):
    """
    Schema for serializing and deserializing Article model data.

    Attributes:
        comments (Nested): Nested field for comments associated with the article.

    Meta:
        model (Article): Specifies the model to be serialized/deserialized.
    """
    # Define a nested field for serializing comments associated with an article
    comments = ma.Nested("CommentSchema", many=True)

    class Meta:
        # Specifies the model to use for the schema
        model = Article








