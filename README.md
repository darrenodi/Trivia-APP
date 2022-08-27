# Trivia-APP
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

Display questions - both all questions and by category. Questions should show the question, category, and difficulty rating by default and can show/hide the answer.
Delete questions.
Add questions and require that they include the question and answer text.
Search for questions based on a text query string.
Play the quiz game, randomizing either all questions or within a specific category.
Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

#About the Stack
We started the full stack application for you. It is designed with some key functional areas:

#Backend
The backend directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in __init__.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

backend/flaskr/__init__.py
backend/test_flaskr.py
View the Backend README for more details.

#Frontend
The frontend directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

What are the end points and HTTP methods the frontend is expecting to consume?
How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?
Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with TODO. These are the files you'd want to edit in the frontend:

frontend/src/components/QuestionView.js
frontend/src/components/FormView.js
frontend/src/components/QuizView.js
By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

View the Frontend README for more details.

#Getting Started
The project frontend is designed to work with Flask-based Backend so it may not load successfully if the backend is not working or not connected.

We recommend the following process:

Stand up the backend
Test backend endpoints using Postman or curl
Stand up the frontend
This should allow the frontend to integrate smoothly.