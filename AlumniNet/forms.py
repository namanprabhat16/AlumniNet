from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    graduation_year = StringField('Graduation Year', validators=[Optional()])
    degree = StringField('Degree', validators=[Optional()])
    current_job = StringField('Current Job', validators=[Optional()])
    company = StringField('Company', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    bio = TextAreaField('Bio', validators=[Optional()])
    linkedin = StringField('LinkedIn URL', validators=[Optional()])
    submit = SubmitField('Save Changes')

class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    location = StringField('Location')
    description = TextAreaField('Job Description', validators=[DataRequired()])
    submit = SubmitField('Post Job')

class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Announcement')