from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Job, Announcement
from forms import RegisterForm, LoginForm, EditProfileForm, JobForm, AnnouncementForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumniNet.db'

from models import db, User
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
@app.route('/directory')
@login_required
def directory():
    q = request.args.get('q', '')
    if q:
        alumni = User.query.filter(
            (User.name.ilike(f'%{q}%')) |
            (User.degree.ilike(f'%{q}%')) |
            (User.location.ilike(f'%{q}%'))
        ).all()
    else:
        alumni = User.query.all()
    return render_template('directory.html', alumni=alumni)
@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    from forms import EditProfileForm
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.graduation_year = form.graduation_year.data
        current_user.degree = form.degree.data
        current_user.current_job = form.current_job.data
        current_user.company = form.company.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        current_user.linkedin = form.linkedin.data
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('profile', user_id=current_user.id))
    elif request.method == 'GET':
        form.graduation_year.data = current_user.graduation_year
        form.degree.data = current_user.degree
        form.current_job.data = current_user.current_job
        form.company.data = current_user.company
        form.location.data = current_user.location
        form.bio.data = current_user.bio
        form.linkedin.data = current_user.linkedin
    return render_template('edit_profile.html', form=form)
@app.route('/jobs')
def job_board():
    jobs = Job.query.order_by(Job.date_posted.desc()).all()
    return render_template('job_board.html', jobs=jobs)


@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            company=form.company.data,
            location=form.location.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('job_board'))
    return render_template('post_job.html', form=form)


@app.route('/delete_job/<int:job_id>')
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        flash('You can only delete your own job posts.', 'danger')
        return redirect(url_for('job_board'))
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted.', 'info')
    return redirect(url_for('job_board'))

@app.route('/announcements')
def announcements():
    all_announcements = Announcement.query.order_by(Announcement.date_posted.desc()).all()
    return render_template('announcements.html', announcements=all_announcements)


@app.route('/post_announcement', methods=['GET', 'POST'])
@login_required
def post_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement posted!', 'success')
        return redirect(url_for('announcements'))
    return render_template('post_announcement.html', form=form)


@app.route('/delete_announcement/<int:announcement_id>')
@login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    if announcement.user_id != current_user.id:
        flash('You can only delete your own announcements.', 'danger')
        return redirect(url_for('announcements'))
    db.session.delete(announcement)
    db.session.commit()
    flash('Announcement deleted.', 'info')
    return redirect(url_for('announcements'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

