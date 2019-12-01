import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

API_PATH = 'http://127.0.0.1:5000/'

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Set up test data
        self.new_question  = {
            'question': 'What is the meaning of life',
            'answer': '42',
            'category': '2',
            'difficulty': 5
        }
        
        self.bad_question  = {
            'question': 'What is the meaning of life',
            'attrubute': 42,
            'difficulty': 5
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

    
    # ---------------------------------------------------------------
    # Get categories
    # ---------------------------------------------------------------
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_categories'],6)
        self.assertEqual(len(data['categories']),6)

    def test_404_error_bad_paramater(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
 
    # ---------------------------------------------------------------
    # Get questions
    # ---------------------------------------------------------------
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
        self.assertEqual(data['message'], 'Resource Not Found')
  

    # ---------------------------------------------------------------
    # delete question
    # ---------------------------------------------------------------
    def test_post_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        # Test to see if question deleted
        questions = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        
        # Asert error if not deleted
        self.assertEqual(questions, None)

    def test_404_delete_question_not_found(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
    
    
    # ---------------------------------------------------------------
    # create question
    # ---------------------------------------------------------------
    def test_create_question(self):
        res = self.client().post('/questions',json=self.new_question)
        data = json.loads(res.data)

        
        question = Question.query.filter(Question.question \
                                         == self.new_question['question']).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(question, None, 'The question was not saved in the db')
        

    def test_405_create_question_fail(self):
        res = self.client().post('/questions/2',json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')


    def test_422_create_question_bad_attributes(self):
        res = self.client().post('/questions',json=self.bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')


    # ---------------------------------------------------------------
    # search questions
    # ---------------------------------------------------------------
    def test_get_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'Anne'} )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']),1)
        self.assertEqual(data['total_questions'], 1)

    def test_search_no_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'xxxxxxxxxxxxx'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
 
 
 
    # ---------------------------------------------------------------
    # Get selected category
    # ---------------------------------------------------------------
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'],20)
        self.assertTrue(len(data['questions']))


    def test_404_error_bad_category_paramater(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    
    
    
    # ---------------------------------------------------------------
    # play quizzes
    # ---------------------------------------------------------------
    def test_get_play_questions(self):
        res = self.client().post('/quizzes', \
                                json={"previous_questions":[],  \
                                "quiz_category":{"type":"Science","id":"0"}} )
                                
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))
        

    def test_no_more_questions(self):
        res = self.client().post('/quizzes', \
                                json={"previous_questions":[20,21,22],  \
                                "quiz_category":{"type":"Science","id":"0"}} )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['question'], None)
     

    
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()