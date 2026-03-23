from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('admin.dashboard' if session.get('role') == 'admin' else 'client.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email, is_active=True).first()
        if not user or not user.check_password(password):
            flash('Credenciais inválidas.', 'danger')
            return render_template('auth/login.html')
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['role'] = user.role
        flash('Login realizado com sucesso.', 'success')
        return redirect(url_for('admin.dashboard' if user.role == 'admin' else 'client.dashboard'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('public.home'))
