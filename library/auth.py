from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import LoginManager

from library.database import Users, db
from library.forms import Registration_Form



bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = Registration_Form()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        new_user = Users(user_name=form.user_name.data)
        new_user.generate_hash(form.user_password.data)
        db.session.add(new_user)
        check_user = Users.query.filter_by(user_name=form.user_name.data).first()

        if check_user is not None:
            error = 'This user already exist'
            flash(error)
            db.session.rollback()
        else:
            db.session.commit()
            return redirect(url_for('auth.login'))

        
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=('POST', 'GET'))
def login():
    return 'Login page'