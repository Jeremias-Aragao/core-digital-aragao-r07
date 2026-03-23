from functools import wraps
from flask import session, redirect, url_for, flash
from app.models import User


def get_current_user():
    user_id = session.get('user_id')
    return User.query.get(user_id) if user_id else None


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            flash('Faça login para continuar.', 'warning')
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    return wrapped


def admin_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            flash('Faça login para continuar.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash('Acesso restrito à área administrativa.', 'danger')
            return redirect(url_for('client.dashboard'))
        return view_func(*args, **kwargs)
    return wrapped
