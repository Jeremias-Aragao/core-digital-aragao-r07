from flask import Blueprint, render_template, session
from app.services.auth_service import login_required
from app.models import Subscription, Module

client_bp = Blueprint('client', __name__, url_prefix='/app')


@client_bp.route('/')
@login_required
def dashboard():
    user_id = session['user_id']
    subscriptions = Subscription.query.filter_by(user_id=user_id, status='active').all()
    active_module_ids = [sub.plan.module_id for sub in subscriptions if sub.plan and sub.plan.module_id]
    modules = Module.query.filter(Module.id.in_(active_module_ids)).all() if active_module_ids else []
    return render_template('client/dashboard.html', subscriptions=subscriptions, modules=modules)
