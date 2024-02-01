from flask import request, jsonify
from app import app, db
from app.models.article import Article
from app.models.comment import Comment
from app.schemas.article_schema import ArticleSchema
from app.schemas.comment_schema import CommentSchema


# Create instances of the data schema classes
article_schema = ArticleSchema()
comment_schema = CommentSchema()

# Set default values for pagination and sorting
DEFAULT_PER_PAGE = 10
DEFAULT_SORT_BY = 'pub_date'
DEFAULT_SORT_ORDER = 'asc'




# Create a new article
@app.route('/api/articles', methods=['POST'])
def create_article():
    """
    Create a new article.

    Parameters:
        None (Data is expected to be in the request's JSON body)

    Returns:
        JSON response with the created article's data and a success message, or an error message on failure.
    """
    try:
        data = request.get_json()

        # Check if required fields are present
        if not all(data.get(key) for key in ['title','content']):
            return jsonify({"message": "Title and content fields are required and cannot be blank"}), 400
        
        # Create a new Article instance
        new_article = Article(
            title=data['title'],
            content=data['content'],
            author=data['author']
        )

        # Add the new article to the database and commit changes
        db.session.add(new_article)
        db.session.commit()

        # Serialize the article data and return a success response
        result=article_schema.dump(new_article)
        return jsonify({"data":result,"message":"Data inserted successfully"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Retrieve a list of articles
@app.route('/api/articles', methods=['GET'])
def get_articles():
    """
    Retrieve a list of articles with optional filters, pagination, and sorting.

    Parameters:
        page (optional): Page number for pagination.
        sort_by (optional): Field to sort by.
        sort_order (optional): Sort order ('asc' or 'desc').
        author_filter (optional): Filter articles by author.
        keyword_filter (optional): Filter articles by keyword.

    Returns:
        JSON response with the list of articles, total count, and a success message, or an error message on failure.
    """
    try:
        # Parse query parameters
        page = request.args.get('page', 1, type=int)
        sort_by = request.args.get('sort_by', DEFAULT_SORT_BY)
        sort_order = request.args.get('sort_order', DEFAULT_SORT_ORDER)  # Default to ascending order
        author_filter = request.args.get('author')
        keyword_filter = request.args.get('keyword')

        # Start building the articles query
        articles_query = Article.query
        
        # Apply author filter if provided
        if author_filter:
            articles_query = articles_query.filter(db.func.lower(Article.author) == author_filter.lower())

        # Apply keyword filter if provided
        if keyword_filter:
            articles_query = articles_query.filter(
                db.or_(
                    Article.title.ilike(f'%{keyword_filter}%'),
                    Article.content.ilike(f'%{keyword_filter}%')
                )
            )
        
        # Apply sorting based on parameters
        if sort_order.lower() == 'desc':
            articles_query = articles_query.order_by(getattr(Article, sort_by).desc())
        else:
            articles_query = articles_query.order_by(getattr(Article, sort_by).asc())
        
        # Count total articles before pagination
        total_article = articles_query.count()
        total_article = total_article if total_article else 0

        # Paginate the query
        articles = articles_query.paginate(page=page, per_page=DEFAULT_PER_PAGE, error_out=False)

        
        # Serialize the articles data and return a success response
        result = article_schema.dump(articles.items, many=True)
        if result:
            return jsonify({"data":result,"total_article":total_article,"message":"Data retrieved successfully"}), 200
        else:
            return jsonify({"data":[],"message":"No articles found"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Retrieve a specific article by ID
@app.route('/api/article/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """
    Retrieve a specific article by ID.

    Parameters:
        article_id: ID of the article to retrieve.

    Returns:
        JSON response with the article data and a success message, or an error message on failure.
    """
    try:
        # Retrieve the article from the database
        article = db.session.get(Article, article_id)
        if article is not None:
            # Serialize the article data and return a success response
            return jsonify({"data":article_schema.dump(article),"message":"Data retrieved successfully"}), 200
        else:
            return jsonify({"data":[],"message":"No articles found with provided id"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Create a new comment for a specific article
@app.route('/api/articles/<int:article_id>/comments', methods=['POST'])
def create_comment(article_id):
    """
    Create a new comment for a specific article.

    Parameters:
        article_id: ID of the article to which the comment belongs.

    Returns:
        JSON response with the created comment's data and a success message, or an error message on failure.
    """

    try:
        data = request.get_json()

        # Check if required fields are present
        if not all(data.get(key) for key in ['author','content']):
            return jsonify({"message": "Author and content fields are required and cannot be blank"}), 400
       
        # Retrieve the article from the database
        article = Article.query.filter_by(id=article_id).first()

        # Create a new Comment instance associated with the article
        if article is not None:
            new_comment = Comment(
                author=data['author'],
                content=data['content'],
                article=article
            )
            # Add the new comment to the database and commit changes
            db.session.add(new_comment)
            db.session.commit()

            # Serialize the comment data and return a success response
            return jsonify({"data":comment_schema.dump(new_comment),"message":"Comment added successfully"}), 201
        else:
            return jsonify({"message": "No articles found with provided id"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Update a specific article by ID
@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    """
    Update a specific article by ID.

    Parameters:
        article_id: ID of the article to update.

    Returns:
        JSON response with the updated article's data and a success message, or an error message on failure.
    """

    try:
        data = request.get_json()
        if data:
            # Retrieve the article from the database
            article = db.session.get(Article, article_id)
            if article is not None:
                # Update article fields if data is provided
                article.title = data.get('title', article.title)
                article.content = data.get('content', article.content)
                article.author = data.get('author', article.author)

                # Commit changes to the database
                db.session.commit()
                
                # Serialize the updated article data and return a success response
                return jsonify({"data":article_schema.dump(article),"message":"Article updated successfully"}), 200
            else:
                return jsonify({"message": "No articles found with provided id"}), 404
        else:
            return jsonify({"message": "No data provided for update"}), 400
    except Exception as e:
        print("e---",e)
        return jsonify({"message": str(e)}), 400



# Delete a specific article by ID 
@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """
    Delete a specific article by ID.

    Parameters:
        article_id: ID of the article to delete.

    Returns:
        JSON response with a success message, or an error message on failure.
    """

    try:
        # Retrieve the article from the database
        article = db.session.get(Article, article_id)

        if article is not None:
            # Delete associated comments first
            Comment.query.filter_by(article_id=article.id).delete()

            # Then delete the article
            db.session.delete(article)
            db.session.commit()

            return jsonify({"message": "Article and associated comments deleted successfully"}), 200
        else:
            return jsonify({"message": "Article not found or already deleted"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    

