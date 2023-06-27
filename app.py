from flask import Flask, render_template, request, redirect, url_for
from scheduler_class import CourseScheduleExtractor

app = Flask(__name__, static_folder='static')

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
    '''
    # Get the current schedule index from the form submission
    current_schedule = int(request.form.get('current_schedule', 0))

    # Adjust the current schedule index based on the button clicked
    if request.form['submit'] == 'prev':
        current_schedule -= 1
    elif request.form['submit'] == 'next':
        current_schedule += 1
    
    # Handle boundary cases where the index goes beyond the schedule list length
    current_schedule = max(0, min(current_schedule, num_schedules - 1))
    '''
    # Pass the data to the template for rendering
    return render_template('schedule.html', schedules=schedules, num_schedules=num_schedules)


if __name__ == '__main__':
    app.run()
