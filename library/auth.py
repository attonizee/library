from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required, current_user

from library.database import Users, db
from library.forms import Registration_Form, Login_Form



bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = Registration_Form()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        new_user = Users(user_name=form.user_name.data)
        new_user.generate_hash(form.user_password.data)
        
        if (Users.query.filter_by(user_name=new_user.user_name).first()) is not None:
            error = 'This user already exist'
            db.session.rollback()
            flash(error)
            
        else:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
                      
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=('POST', 'GET'))
def login():
    form = Login_Form()
    errors = None
    if request.method == 'POST' and form.validate_on_submit():
        check_user = Users.query.filter_by(user_name=form.user_name.data).first()
        if not check_user or not check_user.check_password(form.user_password.data):
            errors = 'Wrong credentials'
        else:
            login_user(check_user, remember=True)
            return redirect(url_for('auth.profile'))

        flash(errors)

    return render_template('auth/login.html', form=form)

@bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', name=current_user)