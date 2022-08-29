import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.username = "postgres"  #Enter your db username
        self.password = "Tantheta%401" #Enter your db password
        self.database_path = "postgresql://{}:{}@{}/{}".format(
    self.username, self.password, "localhost:8080", self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question': 'What does the Q in LGBTQI stand for?',
            'answer': 'Queer',
            'difficulty': 3,
            'category': 1,
            'rating': 1
        }
        self.new_question_error = {
            'question': 'What does the Q in LGBTQI stand for?',
            'difficulty': 3,
            'category': 1,
            'rating': 1
        }

        self.new_category = {
            'category': 'Fiction'
        }
        self.new_category_error = {
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'] > 0,True)
        
    
    def test_422_if_question_creation_fails(self):
        res = self.client().post('/questions', json=self.new_question_error)
        data = json.loads(res.data)
       
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_category(self):
        res = self.client().post('/categories', json=self.new_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_categories'] > 0,True)
        
    
    def test_422_if_category_creation_fails(self):
        res = self.client().post('/categories', json=self.new_category_error)
        data = json.loads(res.data)
       
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_get_question_search_with_results(self):
        res = self.client().post('/questions', json={"search": "Tom"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions']>0,True)
        self.assertIsNotNone((data['questions']))
    
    def test_get_question_search_without_results(self):
        res = self.client().post('/questions', json={"search": "mkbhd"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions']==0,True)
        self.assertIsNotNone((data['questions']))

    def test_get_question_search_error(self):

        res = self.client().post('/questions', json={"searchterm": 'x',})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_questions_based_on_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone((data['questions']))
        self.assertTrue((data['total_questions'] > 0 , True))
        self.assertTrue((data['current_category'] == 3,True))

    def test_questions_based_on_category_error(self):
        res = self.client().get('/categories/category/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_quiz(self):
        new_quiz = {'quiz_category': {'type': 'Science', 'id': 1},'previous_questions': []}

        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_quiz_error(self):
        new_quiz = {'quiz_category': {'type': 'Science', 'id': 1}}
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_delete_question(self):
        new_question = Question(question='What does Q in LGBTQ stand for?', answer='Queer',difficulty=3 , rating=1,category=1)
        new_question.insert()
        res = self.client().delete(f'/questions/{new_question.id}')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == new_question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], (new_question.id))
        self.assertEqual(question, None)
    

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()