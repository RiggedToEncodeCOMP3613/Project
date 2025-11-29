from App.database import db
from App.models.student import Student


def get_leaderboard():
    students = Student.query.all()
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


# Backward compatibility
def view_leaderboard():
    return get_leaderboard()


def generate_leaderboard():
    leaderboard = get_leaderboard()
    # Transform to the expected format
    return [
        {
            'name': entry['username'],
            'hours': entry['total_approved_hours'],
            'student_id': entry['student_id']
        }
        for entry in leaderboard
    ]