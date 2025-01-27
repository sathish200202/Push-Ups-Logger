from flask import Blueprint,  render_template, url_for, request, flash, redirect
#create a blueprint for our app
#render_template used to render the pages
from flask_login import login_required, current_user

from . import db
from .models import Workout, User

main = Blueprint('main', __name__) #this is the blueprint of our app

#get the index page
@main.route('/')
def index():
    
    return render_template('index.html')


#get the profile page
@main.route('/profile')
@login_required
def profile():
    #print(f"current user: {current_user}")
    total_pushups = sum(workout.pushups for workout in current_user.Workout)
    #print(f'pushups: {total_pushups}')
    return render_template('profile.html', user=current_user, total_pushups=total_pushups)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    #print(f'user {user}')

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']

        db.session.commit()

        flash('Profile updated successfully')
        return redirect(url_for('main.profile'))

    return render_template('edit_profile.html', user=user)

#get the create workout page
@main.route('/new-workout')
@login_required
def new_workout():
    return render_template('create_workout.html')

#create new workout
@main.route('/new-workout', methods=['POST'])
@login_required
def new_workout_post():

    pushups = request.form.get('pushups')
    comment = request.form.get('comment')

    try:
        #print(f'pushups: {pushups}, comment: {comment}')
        workout = Workout(pushups=pushups, comment=comment, author=current_user)

        db.session.add(workout)

        db.session.commit()

        flash('Workout added successfully')
        
        return redirect(url_for('main.user_workouts'))
    except Exception as e:
        print(f"Error in creating new workout {e}")

#get the user workouts

@main.route('/all_workouts')
@login_required
def user_workouts():
    #create a page
    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(email=current_user.email).first_or_404()

    workouts = Workout.query.filter_by(author=user).paginate(page=page, per_page=3)

    return render_template('all_workouts.html', workouts=workouts, user=user)


#update the workout
@main.route('/workout/<int:workout_id>/update', methods=['GET', 'POST'])
@login_required
def update_workout(workout_id):
        
    try:
        #get the workout form database using workout id
        workout = Workout.query.get_or_404(workout_id)

        if request.method == 'POST':
            workout.pushups = request.form['pushups']
            workout.comment = request.form['comment']

            db.session.commit()

            flash('Your Workout has been updated!')

            return redirect(url_for('main.user_workouts'))
        return render_template('update_workout.html', workout=workout)
    except Exception as e:
        print(f"Error in update workout {e}")

#delete the workout
@main.route('/workout/<int:workout_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_workout(workout_id):

    try:
        workout = Workout.query.get_or_404(workout_id)

        db.session.delete(workout)
        db.session.commit()

        flash('Workout deleted successfully!')

        return redirect(url_for('main.user_workouts'))
    
    except Exception as e:
        print(f"Error in delete workout {e}")