# from flask_restful import reqparse

# def parse_pagination_args():
#     """
#     Parse pagination arguments for handling page and per_page parameters.

#     Returns:
#         Namespace: Parsed arguments containing 'page' and 'per_page'.
#     """
#     # Create a request parser
#     parser = reqparse.RequestParser()

#     # Add arguments for 'page' and 'per_page' with their types and default values
#     parser.add_argument('page', type=int, default=1)
#     parser.add_argument('per_page', type=int, default=10)

#     # Parse and return the arguments
#     return parser.parse_args()

# def parse_article_args():
#     """
#     Parse arguments for creating a new article.

#     Returns:
#         Namespace: Parsed arguments containing 'title', 'content', and 'author'.
#     """
#     parser = reqparse.RequestParser()

#     # Add arguments for 'title', 'content', and 'author' with their types and requirements
#     parser.add_argument('title', type=str, required=True)
#     parser.add_argument('content', type=str, required=True)
#     parser.add_argument('author', type=str, required=True)
#     return parser.parse_args()

# def parse_comment_args():
#     """
#     Parse arguments for creating a new comment.

#     Returns:
#         Namespace: Parsed arguments containing 'author' and 'content'.
#     """
#     # Create a request parser
#     parser = reqparse.RequestParser()

#     # Add arguments for 'author' and 'content' with their types and requirements
#     parser.add_argument('author', type=str, required=True)
#     parser.add_argument('content', type=str, required=True)
#     return parser.parse_args()

# def parse_update_article_args():
#     """
#     Parse arguments for updating an existing article.

#     Returns:
#         Namespace: Parsed arguments containing 'title', 'content', and 'author'.
#     """
#     # Create a request parser
#     parser = reqparse.RequestParser()
    
#     # Add arguments for 'title', 'content', and 'author' with their types
#     parser.add_argument('title', type=str)
#     parser.add_argument('content', type=str)
#     parser.add_argument('author', type=str)
#     return parser.parse_args()
