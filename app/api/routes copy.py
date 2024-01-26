from flask import request, jsonify
from app import app, db
from app.models.article import Article
from app.models.comment import Comment
from app.schemas.article_schema import ArticleSchema
from app.schemas.comment_schema import CommentSchema
from app.utils.parser import parse_pagination_args, parse_article_args, parse_comment_args, parse_update_article_args

article_schema = ArticleSchema()
comment_schema = CommentSchema()

DEFAULT_PER_PAGE = 10
DEFAULT_SORT_BY = 'pub_date'
DEFAULT_SORT_ORDER = 'asc'


@app.route('/api/articles', methods=['GET'])
def get_articles():
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', DEFAULT_SORT_BY)
    sort_order = request.args.get('sort_order', DEFAULT_SORT_ORDER)  # Default to ascending order
    author_filter = request.args.get('author')
    keyword_filter = request.args.get('keyword')

    articles_query = Article.query
    if author_filter:
        articles_query = articles_query.filter(db.func.lower(Article.author) == author_filter.lower())

    if keyword_filter:
        articles_query = articles_query.filter(
            db.or_(
                Article.title.ilike(f'%{keyword_filter}%'),
                Article.content.ilike(f'%{keyword_filter}%')
            )
        )
    if sort_order.lower() == 'desc':
        articles_query = articles_query.order_by(getattr(Article, sort_by).desc())
    else:
        articles_query = articles_query.order_by(getattr(Article, sort_by).asc())
    
    total_article = articles_query.count()
    total_article = total_article if total_article else 0
    articles = articles_query.paginate(page=page, per_page=DEFAULT_PER_PAGE, error_out=False)

    

    result = article_schema.dump(articles.items, many=True)
    if result:
        return jsonify({"data":result,"total_article":total_article,"message":"Data retrieved successfully"}), 200
    else:
        return jsonify({"data":[],"message":"No articles found"}), 200



@app.route('/api/articles', methods=['POST'])
def create_article():
    data = request.get_json()
    if not all(data.get(key) for key in ['title','content']):
        return jsonify({"message": "Title and content fields are required and cannot be blank"}), 400
    
    new_article = Article(
        title=data['title'],
        content=data['content'],
        author=data.get('author', 'No Name')
    )

    db.session.add(new_article)
    db.session.commit()
    result=article_schema.dump(new_article)
    return jsonify({"data":result,"message":"Data inserted successfully"}), 201



@app.route('/api/article/<int:article_id>', methods=['GET'])
def get_article(article_id):
    print("called get_article")
    article = Article.query.get(article_id)
    if article is not None:
        return jsonify({"data":article_schema.dump(article),"message":"Data retrieved successfully"}), 200
    else:
        return jsonify({"data":[],"message":"No articles found with provided id"}), 200



@app.route('/api/articles/<int:article_id>/comments', methods=['POST'])
def create_comment(article_id):
    
    data = request.get_json()

    if not all(data.get(key) for key in ['author','content']):
        return jsonify({"message": "Author and content fields are required and cannot be blank"}), 400
    
    article = Article.query.get(article_id)
    if article is not None:
        new_comment = Comment(
            author=data['author'],
            content=data['content'],
            article=article
        )

        db.session.add(new_comment)
        db.session.commit()

        return jsonify({"data":comment_schema.dump(new_comment),"message":"Comment added successfully"}), 201
    else:
        return jsonify({"message": "No articles found with provided id"}), 404


@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    
    data = request.get_json()
    article = Article.query.get(article_id)
    print(article)
    if article is not None:
        article.title = data.get('title', article.title)
        article.content = data.get('content', article.content)
        article.author = data.get('author', article.author)

        db.session.commit()

        return jsonify({"data":article_schema.dump(article),"message":"Article updated successfully"}), 200
    else:
        return jsonify({"message": "No articles found with provided id"}), 404
    

@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    article = Article.query.get(article_id)

    if article is not None:
        # Delete associated comments first
        Comment.query.filter_by(article_id=article.id).delete()

        # Then delete the article
        db.session.delete(article)
        db.session.commit()

        return jsonify({"message": "Article and associated comments deleted successfully"}), 200
    else:
        return jsonify({"message": "Article not found or already deleted"}), 400