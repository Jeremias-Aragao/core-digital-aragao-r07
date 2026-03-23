from sqlalchemy import func
from app.models import Module, User, Subscription, FinancialEntry
from app.extensions import db


def admin_metrics():
    return {
        'total_modules': Module.query.count(),
        'active_modules': Module.query.filter_by(is_active=True, is_installed=True).count(),
        'total_users': User.query.count(),
        'active_subscriptions': Subscription.query.filter_by(status='active').count(),
        'total_revenue': db.session.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter(FinancialEntry.entry_type == 'entrada').scalar(),
    }
