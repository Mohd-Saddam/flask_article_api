import unittest
from flask import Flask, json
from unittest.mock import patch, Mock,MagicMock
from app import app, db
from app.models.article import Article
from app.models.comment import Comment
from config import TestingConfig

class APITestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(TestingConfig)
        self.app = app.test_client()

    def tearDown(self):
        pass

    def mock_db_session(self, *args, **kwargs):
        mock_session = Mock()
        if args or kwargs:
            mock_session.query.return_value.get.return_value = args[0]
        return mock_session

    def test_create_article(self):
        with patch('app.api.routes.db.session', new_callable=self.mock_db_session):
            response = self.app.post('/api/articles', json={'title': 'Python', 'content': 'Python Content', 'author': 'Python'})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 201)
            self.assertIn('data', data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Data inserted successfully')

    # def test_get_article(self):
    #     # Create a mock Article object
    #     article = Mock()
    #     article.id = 1
    #     article.title = 'Job'
    #     article.content = 'Job Content'
    #     article.author = 'HR Author'

    #     # Patch the Article.query.get method
    #     with patch('app.models.article.Article.query.get', return_value=article):
    #         response = self.app.get('/api/article/1')
    #         data = json.loads(response.data)

    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn('data', data)
    #         self.assertIn('message', data)
    #         self.assertEqual(data['message'], 'Data retrieved successfully')
    #         self.assertEqual(data['data']['title'], 'Job')
    #         self.assertEqual(data['data']['content'], 'Job Content')

    def test_get_article(self):
        # Create a mock Article object
        article = MagicMock()
        article.id = 1
        article.title = 'Test Title'
        article.content = 'Test Content'
        article.author = 'Test Author'

        with app.app_context():
            with patch('app.models.article.Article.query.get', return_value=article):
                response = self.app.get('/api/article/1')
                data = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertIn('data', data)
                self.assertIn('message', data)
                self.assertEqual(data['message'], 'Data retrieved successfully')


    def test_update_article(self):
        # Create a dictionary representing an article
        article_data = {
            'id': 1,
            'title': 'Test Title',
            'content': 'Test Content',
            'author': 'Test Author'
        }

        # Create a MagicMock to represent the Article class
        article_mock = MagicMock()
        article_mock.query.get.return_value = article_data

        with app.app_context():
            with patch('app.api.routes.db.session', new_callable=self.mock_db_session):
                # Mock the Article class to return the article_mock
                with patch('app.api.routes.Article', article_mock):
                    response = self.app.put('/api/articles/1', json={'title': 'Updated Title', 'content': 'Updated Content'})

                    # Print the raw response content for inspection
                    print("Raw response content:", response.data)

                    try:
                        # Try to parse the response content as JSON
                        data = json.loads(response.data)
                    except json.JSONDecodeError as e:
                        # Print the error if parsing fails
                        print("JSON decoding error:", e)
                        data = None

                    print("Parsed data:", data)

                    # Add checks for response status code and expected data
                    self.assertEqual(response.status_code, 200)

                    if data is not None:
                        self.assertIn('data', data)
                        self.assertIn('message', data)
                        self.assertEqual(data['message'], 'Article updated successfully')
                        self.assertEqual(data['data']['title'], 'Updated Title')
                        self.assertEqual(data['data']['content'], 'Updated Content')





    def test_delete_article(self):
        article = Article(id=1, title='Test Title', content='Test Content', author='Test Author')
        with patch('app.api.routes.db.session', new_callable=self.mock_db_session):
            with patch('app.api.routes.Article', return_value=article):
                response = self.app.delete('/api/articles/1')
                data = json.loads(response.data)

                self.assertEqual(response.status_code, 200)
                self.assertIn('message', data)
                self.assertEqual(data['message'], 'Article and associated comments deleted successfully')

if __name__ == '__main__':
    unittest.main()


