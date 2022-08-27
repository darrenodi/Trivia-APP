import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
  page = request.args.get("page",1,type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
      categories = Category.query.all()
      cat_dict = {}
      for category in categories:
          cat_dict[category.id] = category.type

      # abort 404 if no categories found
      if (len(cat_dict) == 0):
          abort(404)

      # return data to view
      return jsonify({
          'success': True,
          'categories': cat_dict
      })
    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def retrieve_questions():
      categories = Category.query.all()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request,selection)

      if len(current_questions) == 0:
        abort(404)
      
      return jsonify({
        "success":True,
        "questions": current_questions,
        "categories": [cat.type for cat in categories],
        "currentCategory": [],
        "total_questions": len(Question.query.all())
      })
    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
      try:
        
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
          abort(404) 

        question.delete()   
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request,selection)

        return jsonify({
          "success": True,
          "deleted": question_id,
          "questions":current_questions,
          "total_questions": len(Question.query.all())
        })
      
      except:
        abort(422)

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=['POST'])
    def create_question():
      body = request.get_json()
      
      new_question = body.get("question",None)
      new_answer = body.get("answer",None)
      new_difficulty = body.get("difficulty",None)
      new_rating = body.get("rating",None)
      new_category = body.get("category",None)
      if new_answer and new_category and new_rating and new_difficulty and new_answer:
        try:
          question = Question(question=new_question, rating=new_rating, answer=new_answer, difficulty=new_difficulty, category=new_category)
          question.insert()

          selection = Question.query.order_by(Question.id).all()
          current_questions = paginate_questions(request,selection)

          return jsonify({
            "success":True,
            "created":question.id,
            "questions":current_questions,
            "total_questions": len(Question.query.all())
          })

        except:
          abort(422)
      else:
        abort(422)

    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/searchresult", methods=['POST'])
    def search_questions():
      body = request.get_json()
      search = body.get('searchTerm', None)

      try:
        if search:
          selection = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
          current_cat = [question.format() for question in selection]

          return jsonify({
            'success': True,
            'questions':current_cat,
            'total_questions': len(selection),
            'current_category':None # i have no idea what you mean about that ?
          })

      except:
        abort(422)

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:id>/questions",methods=['GET'])
    def get_questions_by_category(id):
      category = Category.query.filter_by(id=id).one_or_none()

      # abort 400 for bad request if category isn't found
      if (category is None):
          abort(400)

      selection = Question.query.filter_by(category=category.id).all()

      # paginate the selection
      paginated = paginate_questions(request, selection)

      # return the results
      return jsonify({
          'success': True,
          'questions': paginated,
          'total_questions': len(Question.query.all()),
          'current_category': category.type
      })
    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        # This endpoint should take category and previous question parameters
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            category_id = quiz_category['id']

            if category_id == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions),
                    Question.category == category_id).all()
            question = None
            if(questions):
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except Exception:
            abort(422)

    """
    CAPABILITY TO CREATE NEW CATEGORIES
    """
    @app.route("/categories", methods=['POST'])
    def create_category():
      body = request.get_json()
      
      new_category = body.get("category",None)

      if new_category:
        try:
          category = Category(type=new_category)
          category.insert()

          categories = Category.query.all()
          cat_dict = {}
          for category in categories:
              cat_dict[category.id] = category.type

          return jsonify({
            "success":True,
            "created":category.id,
            "categories":cat_dict,
            "total_categories": len(Category.query.all())
          })

        except:
          abort(422)
      else:
        abort(422)
    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    return app

