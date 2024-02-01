from flask import request

def parse_pagination_args():
    """Parse pagination arguments from request."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return page, per_page

def parse_article_args():
    """Parse arguments for creating a new article."""
    title = request.json.get('title', type=str)
    content = request.json.get('content', type=str)
    author = request.json.get('author', type=str)
    if not all([title, content, author]):
        raise ValueError("Missing required fields: title, content, author")
    return title, content, author

def parse_comment_args():
    """Parse arguments for creating a new comment."""
    author = request.json.get('author', type=str)
    content = request.json.get('content', type=str)
    if not all([author, content]):
        raise ValueError("Missing required fields: author, content")
    return author, content

def parse_update_article_args():
    """Parse arguments for updating an existing article."""
    title = request.json.get('title', type=str)
    content = request.json.get('content', type=str)
    author = request.json.get('author', type=str)
    return title, content, author
