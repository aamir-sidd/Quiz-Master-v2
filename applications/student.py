from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Quiz, Score, Chapter, Course
from .master import cache

class ViewQuizzesAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=300)
    def get(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 'student':
            return {'message': 'Access denied'}, 403

        quizzes = Quiz.query.join(Chapter).join(Course).all()
        
        quiz_list = []
        for quiz in quizzes:
            quiz_info = {
                'id': quiz.id,
                'chapter_name': quiz.chapter.name,
                'course_name': quiz.chapter.course.name,
                'date_of_quiz': quiz.date_of_quiz.isoformat(),
                'time_duration': quiz.time_duration,
                'remarks': quiz.remarks
            }
            quiz_list.append(quiz_info)
        
        return jsonify(quiz_list)
        
class TakeQuizAPI(Resource):
    @jwt_required()
    @cache.memoize(timeout=300)
    def get(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'student':
            return {'message': 'Access denied'}, 403

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        
        questions = []
        if len(quiz.questions) == 0: 
            return {'message': 'No questions found for this quiz'}, 404
        
        for question in quiz.questions:
            question_data = {
                'id': question.id,
                'question_statement': question.question_statement,
                'option1': question.option1,
                'option2': question.option2,
                'option3': question.option3,
                'option4': question.option4
            }
            questions.append(question_data)
        
        return {'questions': questions, 'time_duration': quiz.time_duration}, 200
        
    @jwt_required()
    def post(self, quiz_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'student':
            return {'message': 'Access denied'}, 403

        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        
        submitted_answers = request.json.get('answers', [])
        
        total_questions = len(quiz.questions)
        if len(submitted_answers) != total_questions:
            return {'message': 'Invalid number of answers'}, 400
        
        total_scored = 0
        detailed_results = []
        
        for i, question in enumerate(quiz.questions):
            user_answer = submitted_answers[i].get('selected_option')
            is_correct = user_answer == question.correct_option
            
            if is_correct:
                total_scored += 1
            
            detailed_results.append({
                'question_id': question.id,
                'selected_option': user_answer,
                'correct_option': question.correct_option,
                'is_correct': is_correct
            })
        
        score_percentage = (total_scored / total_questions) * 100
        
        new_score = Score(
            quiz_id=quiz_id,
            user_id=current_user['id'],
            total_scored=score_percentage
        )
        db.session.add(new_score)
        db.session.commit()
        
        return jsonify({
            'total_questions': total_questions,
            'correct_answers': total_scored,
            'score_percentage': score_percentage,
            'detailed_results': detailed_results
        })
    
class QuizHistoryAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=300)
    def get(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 'student':
            return {'message': 'Access denied'}, 403

        scores = Score.query.filter_by(user_id=current_user['id'])\
            .join(Quiz).join(Chapter).join(Course)\
            .order_by(Score.time_stamp_of_attempt.desc())\
            .all()
        
        quiz_history = []
        for score in scores:
            history_item = {
                'quiz_id': score.quiz_id,
                'course_name': score.quiz.chapter.course.name,
                'chapter_name': score.quiz.chapter.name,
                'score_percentage': score.total_scored,
                'attempt_time': score.time_stamp_of_attempt.isoformat()
            }
            quiz_history.append(history_item)
        
        return jsonify(quiz_history)
        