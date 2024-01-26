
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import ma
from app.models.article import Article

class ArticleSchema(SQLAlchemyAutoSchema):
    comments = ma.Nested("CommentSchema", many=True)

    class Meta:
        model = Article








