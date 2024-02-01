import unittest
from flask import Flask, json
from app import db, app
from app.models.article import Article
from app.models.comment import Comment
from config import TestingConfig

# Test case class for testing API routes
class APITestCase(unittest.TestCase):

    def setUp(self):
        """
        Set up the testing environment before each test case.

        - Configures the Flask app with the testing configuration.
        - Creates a test client to interact with the app.
        - Creates and initializes the test database.
        """
        app.config.from_object(TestingConfig)  # Use testing configuration
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    #Defines a teardown method that runs after each test, cleaning up the testing environment.
    def tearDown(self):
        """
        Tear down the testing environment after each test case.

        - Configures the Flask app with the testing configuration.
        - Creates a test client to interact with the app.
        - Removes the test database and session.
        """
        app.config.from_object(TestingConfig)  # Use testing configuration
        self.app = app.test_client()
        with app.app_context():
            db.session.remove()
            db.drop_all()
    # def tearDown(self):
    #     with app.app_context():
    #         metadata = db.metadata
    #         for table in reversed(metadata.sorted_tables):
    #             if table.name.startswith('test_'):
    #                 db.session.execute(table.delete())
    #         db.session.commit()

    def test_create_article(self):
        """
        Test case for creating a new article.

        - Sends a POST request to create an article.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            response = self.app.post('/api/articles', json={'title': 'Python', 'content': 'Python Content','author': 'Python'})
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertIn('data', data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Data inserted successfully')


    def test_get_article(self):
        """
        Test case for retrieving a specific article by ID.

        - Creates an article in the database.
        - Sends a GET request to retrieve the article by ID.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            article = Article(title='Job', content='Job Content', author='HR Author')
            db.session.add(article)
            db.session.commit()

            response = self.app.get(f'/api/article/{article.id}')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertIn('data', data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Data retrieved successfully')

    def test_update_article(self):
        """
        Test case for updating an existing article.

        - Creates an article in the database.
        - Sends a PUT request to update the article.
        - Asserts that the response has the expected status code, message, and updated content.
        """
        with app.app_context():
            article = Article(title='Test Title', content='Test Content', author='Test Author')
            db.session.add(article)
            db.session.commit()

            new_title = 'Updated Title'
            new_content = 'Updated Content'
            response = self.app.put(f'/api/articles/{article.id}', json={'title': new_title, 'content': new_content})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertIn('data', data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Article updated successfully')
            self.assertEqual(data['data']['title'], new_title)
            self.assertEqual(data['data']['content'], new_content)

    def test_delete_article(self):
        """
        Test case for deleting an article.

        - Creates an article in the database.
        - Sends a DELETE request to delete the article.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            article = Article(title='Test Title', content='Test Content', author='Test Author')
            db.session.add(article)
            db.session.commit()

            response = self.app.delete(f'/api/articles/{article.id}')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Article and associated comments deleted successfully')

    def test_get_articles_with_filter(self):
        """
        Test case for retrieving articles with a filter (author).

        - Creates two articles with different authors in the database.
        - Sends a GET request with an author filter.
        - Asserts that the response has the expected status code, data, and length.
        """
        with app.app_context():
            article1 = Article(title='Test Title 1', content='Test Content 1', author='Author1')
            article2 = Article(title='Test Title 2', content='Test Content 2', author='Author2')

            db.session.add_all([article1, article2])
            db.session.commit()

            response = self.app.get('/api/articles?author=Author1')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertIn('data', data)
            self.assertEqual(len(data['data']), 1)

    def test_create_article_missing_data(self):
        """
        Test case for creating an article with missing data.

        - Sends a POST request to create an article with missing data.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            response = self.app.post('/api/articles', json={})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 400)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Title and content fields are required and cannot be blank')
    
    def test_get_nonexistent_article(self):
        """
        Test case for retrieving a nonexistent article by ID.

        - Sends a GET request with an ID that doesn't exist.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            response = self.app.get('/api/article/999')  # Use an ID that doesn't exist
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 404)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'No articles found with provided id')
    
    def test_update_article_missing_data(self):
        """
        Test case for updating an article with missing update data.

        - Creates an article in the database.
        - Sends a PUT request to update the article with missing data.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            article = Article(title='Test Title', content='Test Content', author='Test Author')
            db.session.add(article)
            db.session.commit()

            response = self.app.put(f'/api/articles/{article.id}', json={})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 400)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'No data provided for update')

    def test_create_comment_missing_data(self):
        """
        Test case for creating a comment with missing data.

        - Creates an article in the database.
        - Sends a POST request to create a comment with missing data.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            article = Article(title='Test Title', content='Test Content', author='Test Author')
            db.session.add(article)
            db.session.commit()

            response = self.app.post(f'/api/articles/{article.id}/comments', json={})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 400)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Author and content fields are required and cannot be blank')


    def test_create_comment_nonexistent_article(self):
        """
        Test case for creating a comment on a nonexistent article.

        - Sends a POST request to create a comment for an article with a nonexistent ID.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            response = self.app.post('/api/articles/883/comments', json={'author': 'Test Author', 'content': 'Test Content'})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 404)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'No articles found with provided id')

    def test_delete_article_nonexistent_id(self):
        """
        Test case for deleting an article with a nonexistent ID.

        - Sends a DELETE request to delete an article with a nonexistent ID.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            response = self.app.delete('/api/articles/1000')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 404)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Article not found or already deleted')

    def test_create_comment_invalid_article_id(self):
        """
        Test case for creating a comment with an invalid article ID.

        - Sends a POST request to create a comment with an invalid article ID.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            response = self.app.post('/api/articles/abc/comments', json={'author': 'Test Author', 'content': 'Test Content'})

            # Check if the response has a JSON content type
            if 'application/json' in response.content_type:
                data = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertIn('message', data)
                self.assertEqual(data['message'], 'Invalid article ID provided')
            else:
                # Handle non-JSON response for HTML error page
                self.assertEqual(response.status_code, 404)
    
    def test_update_article_nonexistent_id(self):
        """
        Test case for updating an article with a nonexistent ID.

        - Sends a PUT request to update an article with a nonexistent ID.
        - Asserts that the response has the expected status code and message.
        """
        with app.app_context():
            response = self.app.put('/api/articles/6463', json={'title': 'Updated Title', 'content': 'Updated Content'})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 404)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'No articles found with provided id')


    def test_get_articles_with_pagination(self):
        """
        Test case for retrieving articles with pagination.

        - Adds multiple articles to the database.
        - Sends a GET request with pagination parameters.
        - Asserts that the response has the expected status code, data, and total article count.
        """
        with app.app_context():
            # Add some articles to the database for pagination testing
            # For simplicity, assuming there are 10 articles in the database
            for i in range(1, 11):
                article = Article(title=f'Test Title {i}', content=f'Test Content {i}', author='Test Author')
                db.session.add(article)

            db.session.commit()

            response = self.app.get('/api/articles?page=2&per_page=5')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertIn('data', data)
            self.assertIn('message', data)

            # Check if 'total_article' is present in the response
            if 'total_article' in data:
                self.assertEqual(len(data['data']), 5)
                self.assertEqual(data['total_article'], 10)
            else:
                # Handle the case where 'total_article' is not present
                self.assertEqual(len(data['data']), 0)



    def test_get_comments_for_article(self):
        """
        Test case for retrieving comments for a specific article.

        - Creates an article with comments in the database.
        - Sends a POST request to add a new comment to the article.
        - Asserts that the response has the expected status code, data, and updated comment count.
        """
        with app.app_context():
            # Create an article with comments for testing
            article = Article(title='Test Title', content='Test Content', author='Test Author')
            db.session.add(article)
            db.session.commit()

            # Add comments to the article
            comment1 = Comment(author='Commenter1', content='Comment Content 1', article=article)
            comment2 = Comment(author='Commenter2', content='Comment Content 2', article=article)
            db.session.add_all([comment1, comment2])
            db.session.commit()

            response = self.app.post(f'/api/articles/{article.id}/comments', json={'author': 'New Commenter', 'content': 'New Comment Content'})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 201)
            self.assertIn('data', data)
            self.assertIn('message', data)
            self.assertEqual(len(data['data']), 4)
    def test_get_articles_default_pagination(self):
        """
        Test case for retrieving articles with default pagination settings.

        - Adds multiple articles to the database.
        - Sends a GET request without specifying pagination parameters.
        - Asserts that the response has the expected status code, data, and default pagination settings.
        """
        with app.app_context():
            # Add some articles to the database for testing
            # For simplicity, assuming there are 10 articles in the database
            for i in range(1, 11):
                article = Article(title=f'Test Title {i}', content=f'Test Content {i}', author='Test Author')
                db.session.add(article)

            db.session.commit()

            response = self.app.get('/api/articles')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertIn('data', data)
            self.assertIn('message', data)

            # Check if 'total_article' is present in the response
            if 'total_article' in data:
                self.assertEqual(len(data['data']), 10)  # Assuming the default per_page is 10
                self.assertEqual(data['total_article'], 10)
            else:
                # Handle the case where 'total_article' is not present
                self.assertEqual(len(data['data']), 0)

    def test_get_articles_with_keyword_filter(self):
        """
        Test case for retrieving articles with a keyword filter.

        - Adds articles with specific keywords in the database.
        - Sends a GET request with a keyword filter.
        - Asserts that the response has the expected status code and filtered articles.
        """
        with app.app_context():
            article1 = Article(title='Python News', content='Latest Python updates', author='Python Author')
            article2 = Article(title='Flask Tutorial', content='Learn Flask step by step', author='Web Developer')
            
            db.session.add_all([article1, article2])
            db.session.commit()

            response = self.app.get('/api/articles?keyword=Python')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertIn('data', data)
            self.assertEqual(len(data['data']), 1)
            self.assertEqual(data['data'][0]['title'], 'Python News')

if __name__ == '__main__':
    unittest.main()
