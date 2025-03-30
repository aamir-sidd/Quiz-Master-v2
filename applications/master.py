from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_caching import Cache
from .models import db, Course, Chapter, Quiz, Question
from datetime import datetime

cache = Cache()

class CourseAPI(Resource):
    # Getting all courses
    @jwt_required()
    @cache.cached(timeout=300)
    def get(self):
        courses = Course.query.all()
        return jsonify([{
            'id': course.id,
            'name': course.name,
            'description': course.description
        } for course in courses])

    # Create a new course
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        data = request.get_json()
        if not data.get('name') or not data.get('description'):
            return {'message': 'Name and Description are required'}, 400

        if Course.query.filter_by(name=data['name']).first():
            return {'message': 'Course with this name already exists'}, 409

        new_course = Course(name=data['name'], description=data['description'])
        db.session.add(new_course)
        db.session.commit()
        return {'message': 'Course created successfully', 'course_id': new_course.id}, 201

class CourseDetailAPI(Resource):
    @jwt_required()
    @cache.memoize(timeout=300)
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        return {
            'id': course.id,
            'name': course.name,
            'description': course.description
        }

    # Updating any course
    @jwt_required()
    def put(self, course_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        data = request.get_json()
        course.name = data.get('name', course.name)
        course.description = data.get('description', course.description)
        db.session.commit()

        return {'message': 'Course updated successfully'}

    # Deleting any specific course
    @jwt_required()
    def delete(self, course_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        db.session.delete(course)
        db.session.commit()

        return {'message': 'Course deleted successfully'}

class ChapterAPI(Resource):
    # Getting all chapters for a specific course  
    @jwt_required()  
    @cache.cached(timeout=300)
    def get(self):
        chapters = Chapter.query.all()
        return jsonify([{
            'id': chapter.id,
            'name': chapter.name,
            'course_id': chapter.course_id,
            'course_name': chapter.course.name,
            'description': chapter.description
        } for chapter in chapters])

    # Creating a new chapter for a specific course
    @jwt_required()
    def post(self, course_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        data = request.get_json()
        if not data.get('name') or not data.get('description'):
            return {'message': 'Name and Description are required'}, 400

        new_chapter = Chapter(name=data['name'], description=data['description'], course=course)
        db.session.add(new_chapter)
        db.session.commit()
        return {'message': 'Chapter created successfully', 'chapter_id': new_chapter.id}, 201

class ChapterDetailAPI(Resource):
    # Get a specific chapter by ID
    @jwt_required()
    @cache.memoize(timeout=300)
    def get(self, chapter_id):
        chapter = Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        return {
            'id': chapter.id,
            'course_id': chapter.course_id,
            'course_name': chapter.course.name,
            'name': chapter.name,
            'description': chapter.description
        }
    
    # to Update a specific chapter
    @jwt_required()
    def put(self, chapter_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        chapter = Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        data = request.get_json()
        chapter.name = data.get('name', chapter.name)
        chapter.description = data.get('description', chapter.description)
        db.session.commit()

        return {'message': 'Chapter updated successfully'}
    
    # for delete a specific chapter
    @jwt_required()
    def delete(self, chapter_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        chapter = Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        db.session.delete(chapter)        
        db.session.commit()

        return {'message': 'Chapter deleted successfully'}

class QuizAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=300)
    def get(self):
        quizzes = Quiz.query.all()
        return jsonify([{
            'id': quiz.id,
            'chapter_id': quiz.chapter_id,
            'chapter_name': quiz.chapter.name,
            'date_of_quiz': quiz.date_of_quiz,
            'time_duration': quiz.time_duration,
            'remarks': quiz.remarks
        } for quiz in quizzes])
    
    # for Create a new quiz for a specific chapter
    @jwt_required()
    def post(self, chapter_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        chapter = Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        data = request.get_json()
        if not data.get('date_of_quiz') or not data.get('time_duration'):
            return {'message': 'Date of Quiz and Time Duration are required'}, 400

        try:
            quiz_date = datetime.strptime(data['date_of_quiz'], '%Y-%m-%d').date()
        except ValueError:
            return {'message': 'Invalid date format. Use YYYY-MM-DD'}, 400

        new_quiz = Quiz(date_of_quiz=quiz_date, 
                        time_duration=data['time_duration'], 
                        chapter=chapter, 
                        remarks=data.get('remarks'))
        db.session.add(new_quiz)
        db.session.commit()

        return {'message': 'Quiz created successfully', 'quiz_id': new_quiz.id}, 201
    
class QuizDetailAPI(Resource):
    # Get a specific quiz by ID
    @jwt_required()
    @cache.memoize(timeout=300)
    def get(self, quiz_id):
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        return {
            'id': quiz.id,
            'date_of_quiz': quiz.date_of_quiz,
            'time_duration': quiz.time_duration,
            'remarks': quiz.remarks
        }
    
    # Update a specific quiz
    @jwt_required()
    def put(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        data = request.get_json()
        print(data.get('date_of_quiz'))
        print(quiz.date_of_quiz)
        if data.get('date_of_quiz') != quiz.date_of_quiz:
            quiz.date_of_quiz = datetime.strptime(data['date_of_quiz'], '%Y-%m-%d').date()
            
        
        quiz.time_duration = data.get('time_duration', quiz.time_duration)
        quiz.remarks = data.get('remarks', quiz.remarks)
        db.session.commit()

        return {'message': 'Quiz updated successfully'}
    
    # Delete a specific quiz
    @jwt_required()
    def delete(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        db.session.delete(quiz)        
        db.session.commit()

        return {'message': 'Quiz deleted successfully'}
    
class QuestionAPI(Resource):
    @jwt_required()
    @cache.memoize(timeout=300)
    def get(self, quiz_id):
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        questions = quiz.questions
        return jsonify([{
            'id': question.id,
            'question_statement': question.question_statement,
            'option1': question.option1,
            'option2': question.option2,
            'option3': question.option3,
            'option4': question.option4,
            'correct_option': question.correct_option
        } for question in questions])

    @jwt_required()
    def post(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        data = request.get_json()
        new_question = Question(
            quiz_id=quiz.id,
            question_statement=data.get('question_statement'),
            option1=data.get('option1'),
            option2=data.get('option2'),
            option3=data.get('option3'),
            option4=data.get('option4'),
            correct_option=data.get('correct_option')
        )
        db.session.add(new_question)
        db.session.commit()
        return {'message': 'Question created successfully', 'question_id': new_question.id}, 201

class QuestionDetailAPI(Resource):
    @jwt_required()
    @cache.memoize(timeout=300)
    def get(self, question_id):
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return {'message': 'Question not found'}, 404

        return {
            'id': question.id,
            'question_statement': question.question_statement,
            'option1': question.option1,
            'option2': question.option2,
            'option3': question.option3,
            'option4': question.option4,
            'correct_option': question.correct_option
        }

    @jwt_required()
    def put(self, question_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return {'message': 'Question not found'}, 404

        data = request.get_json()
        question.question_statement = data.get('question_statement', question.question_statement)
        question.option1 = data.get('option1', question.option1)
        question.option2 = data.get('option2', question.option2)
        question.option3 = data.get('option3', question.option3)
        question.option4 = data.get('option4', question.option4)
        question.correct_option = data.get('correct_option', question.correct_option)
        db.session.commit()

        return {'message': 'Question updated successfully'}

    @jwt_required()
    def delete(self, question_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return {'message': 'Access denied'}, 403

        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return {'message': 'Question not found'}, 404

        db.session.delete(question)
        db.session.commit()

        return {'message': 'Question deleted successfully'}
