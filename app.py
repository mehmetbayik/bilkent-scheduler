from flask import Flask, render_template, request, redirect, url_for, session
from scheduler_class import CourseScheduleExtractor
import pandas as pd

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')


# ... Your other routes and functions ...

@app.route('/schedule', methods=['POST'])
def schedule():
    # Retrieve form data
    course = ['', '', '', '', '', '']
    course[0] = request.form['course1']
    course[1] = request.form['course2']
    course[2] = request.form['course3']
    course[3] = request.form['course4']
    course[4] = request.form['course5']
    course[5] = request.form['course6']
    # ... retrieve other form inputs as needed
    courses = []
    for i in range(6):
        if course[i] != '':
            courses.append(course[i])

    # Use your class to generate the course combinations
    schedule_string = open('data.txt','r').read()
    scheduler = CourseScheduleExtractor(schedule_string, courses)

    # Generate the schedules and retrieve necessary data
    schedules = scheduler.get_schedules()
    num_schedules = len(schedules)

    # Convert the DataFrame to a list of dictionaries
    schedules_json = []
    for schedule in schedules:
        schedules_json.append(schedule.to_dict(orient='records'))

    # Store the schedules and num_schedules in the session
    session['schedules'] = schedules_json
    session['num_schedules'] = num_schedules

    # Redirect to the schedules route
    return redirect(url_for('schedules'))

@app.route('/schedules', methods=['GET', 'POST'])
def schedules():
    # Retrieve the schedules and num_schedules from the session
    schedules_json = session.get('schedules', [])
    num_schedules = session.get('num_schedules', 0)

    # Convert the schedules back to DataFrame
    schedules = []
    for schedule in schedules_json:
        schedules.append(pd.DataFrame(schedule))

    # Get the current schedule index from the session
    current_schedule = session.get('current_schedule', 0)

    # Adjust the current schedule index based on the button clicked
    if request.method == 'POST':
        if request.form['submit'] == 'prev':
            current_schedule = max(0, current_schedule - 1)
        elif request.form['submit'] == 'next':
            current_schedule = min(current_schedule + 1, num_schedules - 1)

    # Update the current schedule index in the session
    session['current_schedule'] = current_schedule

    # Render the schedule template with the current schedule
    return render_template('schedule.html', schedules=schedules, num_schedules=num_schedules, current_schedule=current_schedule)


if __name__ == '__main__':
    app.run()
