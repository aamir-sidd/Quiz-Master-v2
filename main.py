from flask import Flask, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from applications.models import db, User
from applications.master import CourseAPI, CourseDetailAPI, ChapterAPI, ChapterDetailAPI
from applications.master import QuizAPI, QuizDetailAPI, QuestionAPI, QuestionDetailAPI, cache 
from applications.student import ViewQuizzesAPI, TakeQuizAPI, QuizHistoryAPI
from applications.auth import UserRegistrationAPI, UserLoginAPI
from applications.worker import *
from applications.task import *

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'masters_secret'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=18)  
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379"
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

jwt = JWTManager(app)
api = Api(app)
db.init_app(app)
cache.init_app(app)
app.app_context().push()

celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/1',
    timezone = 'Asia/Kolkata'
)

api.add_resource(CourseAPI, '/admin/courses')
api.add_resource(CourseDetailAPI, '/admin/courses/<int:course_id>')
api.add_resource(ChapterAPI, '/admin/chapters', '/admin/chapter/<int:course_id>')
api.add_resource(ChapterDetailAPI, '/admin/chapter/<int:chapter_id>')
api.add_resource(QuizAPI, '/admin/quizzes', '/admin/quiz/<int:chapter_id>',)
api.add_resource(QuizDetailAPI, '/admin/quiz/<int:quiz_id>')
api.add_resource(QuestionAPI, '/admin/questions/<int:quiz_id>', '/admin/question/<int:quiz_id>')
api.add_resource(QuestionDetailAPI, '/admin/question/<int:question_id>')
api.add_resource(ViewQuizzesAPI, '/student/quizzes')
api.add_resource(TakeQuizAPI, '/student/quiz/<int:quiz_id>')
api.add_resource(QuizHistoryAPI, '/student/quiz-history')
api.add_resource(UserRegistrationAPI, '/auth/register')
api.add_resource(UserLoginAPI, '/auth/login')

@app.before_request
def clear_cache():
    if request.method != 'GET':
        cache.clear()

def create_admin():
    if not User.query.filter_by(role='admin').first():
        admin_user = User(
            full_name="Admin",
            email="admin@gmail.com",
            password='admin',
            role='admin' 
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully")

if __name__ == '__main__':
    db.create_all()
    create_admin()
    app.run(debug=True)