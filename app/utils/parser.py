from flask_restful import reqparse

def parse_pagination_args():
    parser = reqparse.RequestParser()
    parser.add_argument('page', type=int, default=1)
    parser.add_argument('per_page', type=int, default=10)
    return parser.parse_args()

def parse_article_args():
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True)
    parser.add_argument('content', type=str, required=True)
    parser.add_argument('author', type=str, required=True)
    return parser.parse_args()

def parse_comment_args():
    parser = reqparse.RequestParser()
    parser.add_argument('author', type=str, required=True)
    parser.add_argument('content', type=str, required=True)
    return parser.parse_args()

def parse_update_article_args():
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('content', type=str)
    parser.add_argument('author', type=str)
    return parser.parse_args()
