from flask import Blueprint, render_template, redirect, request, url_for, flash


bp = Blueprint('lib', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('lib/index.html')