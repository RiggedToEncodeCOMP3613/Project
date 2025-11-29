from App.database import db
from App.models.student import Student


def view_leaderboard():
    students = db.session.scalars(db.select(Student)).all()
    leaderboard = []
    for student in students:
        total_hours = student.total_hours
        leaderboard.append({
            'student_id': student.student_id,
            'username': student.username,
            'total_approved_hours': total_hours
        })
    leaderboard.sort(key=lambda x: x['total_approved_hours'], reverse=True)
    return leaderboard


def generate_leaderboard():
    students = Student.query.all()
    leaderboard = []
    for student in students:
        total_hours = student.total_hours

        leaderboard.append({
            'name': student.username,
            'hours': total_hours,
            'student_id': student.student_id
        })

    leaderboard.sort(key=lambda item: item['hours'], reverse=True)

    return leaderboard