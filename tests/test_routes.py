import unittest
from flask import Flask, json
from app import db, app
from app.models.article import Article
from app.models.comment import Comment

class APITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_article(self):
        with app.app_context():
            response = self.app.post('/api/articles', json={'title': 'Python', 'content': 'Python Content','author': 'Python'})
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertIn('data', data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Data inserted successfully')


    def test_get_article(self):
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
        with app.app_context():
            response = self.app.post('/api/articles', json={})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 400)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Title and content fields are required and cannot be blank')
    
    def test_get_nonexistent_article(self):
        with app.app_context():
            response = self.app.get('/api/article/999')  # Use an ID that doesn't exist
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 404)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'No articles found with provided id')
    
    def test_update_article_missing_data(self):
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
        with app.app_context():
            response = self.app.post('/api/articles/883/comments', json={'author': 'Test Author', 'content': 'Test Content'})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 404)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'No articles found with provided id')

    def test_delete_article_nonexistent_id(self):
        with app.app_context():
            response = self.app.delete('/api/articles/1000')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 404)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Article not found or already deleted')

    def test_create_comment_invalid_article_id(self):
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
        with app.app_context():
            response = self.app.put('/api/articles/6463', json={'title': 'Updated Title', 'content': 'Updated Content'})
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 404)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'No articles found with provided id')


    def test_get_articles_with_pagination(self):
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


if __name__ == '__main__':
    unittest.main()
