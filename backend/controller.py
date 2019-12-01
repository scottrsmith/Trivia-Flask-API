"""
**Introduction**
----------------

The Trivia API includes multiple REST methods.
These methods are to create, list, and search questions as well as perform
operationsto list by category and search. The Quizzes API is for playing the
game.

- Create or Search Questions. This API will create a new question or search
questions.
- Retrieve Questions. This API will retrieve a page of 10 trivia questions
sorted by question_id.
- Delete Question. This API will delete a question from the database.
- Retrieve Category. This API will retrieve a list of trivia categories.
- Retrieve Category Questions. This API will retrieve a list of questions
by category Id.
- Play Quiz. This API will play the quiz. Presenting a random, non-repeated
question in the category.
"""

import os
from flask import Flask, request, abort, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# ----------------------------------------------------------------------------#
# Helper Functions
#    dump: print out the contents of an object
#    paginate: pages data for output
#    leftJoin does a database left join on sets
# ----------------------------------------------------------------------------#


def dumpObj(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def dumpData(obj):
    for attr in obj:
        print("data.%s = %r" % (attr, obj[attr]))


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


# Left join two sets, as lists
def leftJoin(left, right):
    joined_list = []
    for x in left:
        if x not in right:
            joined_list.append(x)
    # print ('left: {}, right: {}, joined:{}'.format(left, right, joined_list))
    return joined_list


trivia_api = Blueprint('trivia_api', __name__)


# ----------------------------------------------------------------------------#
#  Create or Search questions
# ----------------------------------------------------------------------------#
trivia_api.route('/questions', methods=['POST'])


def create_or_search_question():
    """
        **Create or Search Questions**

        This API will create a new question or search questions.

        **Create a new question**

        - Sample Call create question::

            curl -X POST http://localhost:5000/questions
                 -H 'content-type: application/json'
                 -d '{"question":"One plus one is","answer":"2","difficulty":1
                     ,"category":1}'

        - Expected Success Response::

            HTTP Status Code: 200

            {
             "success": true
            }


        - Expected Fail Response::

            HTTP Status Code: 404
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }

        **Search Questions**

        - Sample Call search question::

            curl -X POST http://localhost:5000/questions
                 -H 'content-type: application/json'
                 -d '{"searchTerm":"Anne"}'

        - Expected Success Response::

            HTTP Status Code: 200
            {
             "questions": [
                {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 4,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, "\
                             "then praise in the role of her beloved Lestat?"
                }
             ],
             "success": true,
             "total_questions": 1
            }

        - Search not found::

            HTTP Status Code: 200

            {
             "questions": [],
             "success": true,
             "total_questions": 0
            }
    """
    request_json = request.get_json()
    search = request_json.get('searchTerm', None)

    try:
        if search:
            selection = Question.query.order_by(Question.id).filter(
                            Question.question.ilike('%{}%'.format(search)))
            current_questions = paginate_questions(request, selection)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection.all())
            })

        else:
            # The request JSON is passed to be initialized by Question
            # class's __init__
            question = Question(request_json)
            question.insert()

            return jsonify({
                'success': True
            })
    except Exception:
        abort(422)


# ----------------------------------------------------------------------------#
#  Retrieve API Questions
# ----------------------------------------------------------------------------#
@trivia_api.route('/questions', methods=['GET'])
def retrieve_questions():
    """
        **Retrieve API Questions**

        This API will retrieve a page of 10 trivia questions sorted by
        question_id. Pages are designated by the 'page' url parameter.

        - Sample Call::

            curl -X GET http://localhost:5000/questions?page=1
                 -H 'content-type: application/json'

        - Expected Success Response::

            HTTP Status Code: 200

            {
                "categories": [
                    "Science",
                    "Art",
                    "Geography",
                    "History",
                    "Entertainment",
                    "Sports"
                ],
                "current_category": 5,
                "questions": [
                    {
                    "answer": "Apollo 13",
                    "category": 5,
                    "difficulty": 4,
                    "id": 2,
                    "question": "What movie earned Tom Hanks his third " \
                                "straight Oscar nomination, in 1996?"
                    },
                    {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the " \
                                "Hall of Mirrors?"
                    }
                ],
                "success": true,
                "total_questions": 20
            }

        - Expected Fail Response::

            HTTP Status Code: 404
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
    """

    current_category = 5
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all()),
        'current_category': current_category,
        'categories': [cat.type for cat in Category.query.all()]
    })


# ----------------------------------------------------------------------------#
#  Delete question from the database
# ----------------------------------------------------------------------------#
trivia_api.route('/questions/<int:question_id>', methods=['DELETE'])


def delete_question(question_id):
    """
        **Delete a Question from the database**

        This API will delete a question from the database.

        - Sample Call::

            curl -X DELETE http://localhost:5000/questions/2
                 -H 'content-type: application/json'

        - Expected Success Response::

            HTTP Status Code: 200
            {
                "deleted": 2,
                "success": true
            }


        - Expected Fail Response::

            HTTP Status Code: 422
            {
             "error": 422,
             "message": "unprocessable",
             "success": false
            }
    """
    try:
        question = Question.query.filter(Question.id
                                         == question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'success': True,
            'deleted': question_id
        })

    except Exception:
        abort(422)


# ----------------------------------------------------------------------------#
#  Retrieve Trivia Categories
# ----------------------------------------------------------------------------#
@trivia_api.route('/categories', methods=['GET'])
def retrieve_category():
    """
        **Retrieve Trivia Categories**

        This API will retrive a list of trivia categories.

        - Sample Call::

            curl -X GET http://localhost:5000/categories
                 -H 'content-type: application/json'

        - Expected Success Response::

            HTTP Status Code: 200

            {
                "categories": [
                                "Science",
                                "Art",
                                "Geography",
                                "History",
                                "Entertainment",
                                "Sports"
                                ],
                "success": true,
                "total_categories": 6
            }

        - Expected Fail Response::

            HTTP Status Code: 404
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
    """

    selection = Category.query.order_by(Category.id).all()

    if len(selection) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'categories': [cat.type for cat in selection],
        'total_categories': len(selection)
    })


# ----------------------------------------------------------------------------#
#  Retrieve Category Questions
# ----------------------------------------------------------------------------#
@trivia_api.route('/categories/<int:category_id>/questions', methods=['GET'])
def retrieve_category_questions(category_id):
    """
        **Retrieve Category Questions**

        This API will retrieve a list of questions by category Id.

        - Sample Call::

            curl -X GET http://localhost:5000/categories/1/questions
                 -H 'content-type: application/json'

        - Expected Success Response::

            HTTP Status Code: 200

            {
            "current_category": 2,
            "questions": [
                {
                "answer": "Escher",
                "category": 2,
                "difficulty": 1,
                "id": 16,
                "question": "Which Dutch graphic artist initials M C was a " \
                            "creator of optical illusions?"
                },
                {
                "answer": "Jackson Pollock",
                "category": 2,
                "difficulty": 2,
                "id": 19,
                "question": "Which American artist was a pioneer of " \
                            "Abstract Expressionism, and a leading exponent " \
                            "of action painting?"
                }
            ],
            "success": true,
            "total_questions": 24
            }


        - Expected Fail Response::

            HTTP Status Code: 404
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
    """
    # Fix the category from what the front end sent.
    category_id += 1
    selection = Question.query.filter(Question.category == category_id).all()
    current_questions = paginate_questions(request, selection)
    # Abort if no questions
    if len(current_questions) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all()),
        'current_category': category_id,
    })


# ----------------------------------------------------------------------------#
#  Play Quiz
# ----------------------------------------------------------------------------#
@trivia_api.route('/quizzes', methods=['POST'])
def quizzes():
    """
        **Play Quiz**

        This API will play the quiz. Presenting a random, non-repeated
        question in the category.

        - Sample Call::

            curl -X POST http://localhost:5000/quizzes
                 -H 'content-type: application/json'
                 -d '{"previous_questions":[]
                      ,"quiz_category":{"type":"Science","id":"0"}}'


        - Expected Success Response::

            HTTP Status Code: 200

            {
            "question": {
                "answer": "The Liver",
                "category": 1,
                "difficulty": 4,
                "id": 20,
                "question": "What is the heaviest organ in the human body?"
            },
            "success": true
            }


        - Expected Fail Response::

            HTTP Status Code: 404
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
    """
    body = request.get_json()
    quiz_category = body.get('quiz_category', None)
    if quiz_category is not None:
        previous_questions = body.get('previous_questions', [])
    if quiz_category['type'] == 'click':
        # only select questions that are not in previous
        selection = Question.query.filter(
                                   ~Question.id.in_(previous_questions)).all()
    else:
        # Fix the category ID
        category = int(quiz_category['id']) + 1
        # only select questions that are not in previous in selectged category
        selection = Question.query.filter(
                        Question.category == category,
                        ~Question.id.in_(previous_questions)).all()

    rows_returned = len(selection)
    if rows_returned == 0:
        return jsonify({'success': False,
                        'question': None})

    else:
        # Get a random nummber for the return array to select a question
        pick = int(random.random() * rows_returned)

    return jsonify({'success': True,
                    'question': selection[pick].format()})
