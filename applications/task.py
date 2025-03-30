from .worker import celery
from .models import User, Score, Quiz, Chapter, Course
from celery.schedules import crontab
from jinja2 import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, monthly_report.s(), name='Test Report every 10s')
    sender.add_periodic_task(10.0, daily_reminder.s(), name='Test reminder every 10s')

    sender.add_periodic_task(
        crontab(hour=18, minute=30),
        daily_reminder.s(),
        name='Daily reminder at 6:30 p.m.'
    )

    sender.add_periodic_task(
        crontab(day_of_month='1', month_of_year='*'),
        monthly_report.s(),
        name='Monthly report on 1st of every month.'
    )


def send_mail(email, subject, email_content, attachment=None):
    smtp_server_host = "localhost"

    msg = MIMEMultipart()
    msg["From"] = "admin@masterquiz.com"
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(email_content, "html"))

    if attachment:
        with open(attachment, "rb") as attachment_content:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_content.read())
            encoders.encode_base64(part)
        print(os.path.basename(attachment))
        part.add_header('Content-Disposition', f'attachment; filename= "{os.path.basename(attachment)}"')
        msg.attach(part)

    server = smtplib.SMTP(host=smtp_server_host, port=1025)
    server.login("admin@masterquiz.com", "")
    server.send_message(msg)
    server.quit()
    print("Mail sent")

def generate_html_report(name, data):
    with open("applications/report/report.html", "r") as file:
        jinja_template = Template(file.read())
        html_report = jinja_template.render(name=name, data=data)
        return html_report

@celery.task
def daily_reminder():
    users = User.query.filter_by(role='student').all()
    for user in users:
        msg = f'<h3>Hi {user.full_name}! Please check our platform for the latest quizzes and updates.</h3>'
        send_mail(email=user.email, email_content=msg, subject="Daily Reminder")
    print('Reminder Sent!')

@celery.task
def monthly_report():
    users = User.query.filter_by(role='student').all()
    for user in users:
        scores = Score.query.filter_by(user_id=user.id).all()
        report_data = []
        
        for score in scores:
            quiz = Quiz.query.get(score.quiz_id)
            chapter = Chapter.query.get(quiz.chapter_id)
            course = Course.query.get(chapter.course_id)
            
            temp_data = [
                score.id,
                course.name,
                chapter.name,
                quiz.date_of_quiz,
                quiz.time_duration,
                score.total_scored
            ]
            report_data.append(temp_data)
        
        html_report = generate_html_report(name=user.full_name, data=report_data)
        send_mail(email=user.email, email_content=html_report, subject="Monthly Report")
    print("Monthly Reports Sent!")
