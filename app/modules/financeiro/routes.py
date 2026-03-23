from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.auth_service import login_required
from app.models import FinancialEntry, Subscription, Plan, Module
from app.extensions import db

financeiro_bp = Blueprint('financeiro', __name__, url_prefix='/modulos/financeiro')


def has_financial_access(user_id: int) -> bool:
    module = Module.query.filter_by(slug='financeiro').first()
    if not module:
        return False
    return Subscription.query.join(Plan).filter(
        Subscription.user_id == user_id,
        Subscription.status == 'active',
        Plan.module_id == module.id,
    ).count() > 0 or session.get('role') == 'admin'


@financeiro_bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    if not has_financial_access(user_id):
        flash('Você não possui acesso ao módulo financeiro.', 'danger')
        return redirect(url_for('client.dashboard'))
    entries = FinancialEntry.query.filter_by(user_id=user_id).order_by(FinancialEntry.reference_date.desc(), FinancialEntry.id.desc()).all()
    total_entries = db.session.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter_by(user_id=user_id, entry_type='entrada').scalar()
    total_exits = db.session.query(func.coalesce(func.sum(FinancialEntry.amount), 0.0)).filter_by(user_id=user_id, entry_type='saida').scalar()
    return render_template('modules/financeiro/index.html', entries=entries, saldo=total_entries-total_exits, total_entries=total_entries, total_exits=total_exits)


@financeiro_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def create_entry():
    user_id = session['user_id']
    if not has_financial_access(user_id):
        flash('Você não possui acesso ao módulo financeiro.', 'danger')
        return redirect(url_for('client.dashboard'))
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        entry_type = request.form.get('entry_type', '').strip()
        amount_raw = request.form.get('amount', '').replace(',', '.').strip()
        reference_date_raw = request.form.get('reference_date', '').strip()
        notes = request.form.get('notes', '').strip()
        try:
            amount = float(amount_raw)
            reference_date = datetime.strptime(reference_date_raw, '%Y-%m-%d').date()
        except ValueError:
            flash('Valor ou data inválidos.', 'danger')
            return render_template('modules/financeiro/form.html')
        entry = FinancialEntry(user_id=user_id, description=description, category=category, entry_type=entry_type, amount=amount, reference_date=reference_date, notes=notes)
        db.session.add(entry)
        db.session.commit()
        flash('Lançamento cadastrado com sucesso.', 'success')
        return redirect(url_for('financeiro.index'))
    return render_template('modules/financeiro/form.html')


@financeiro_bp.route('/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = FinancialEntry.query.filter_by(id=entry_id, user_id=session['user_id']).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    flash('Lançamento removido.', 'info')
    return redirect(url_for('financeiro.index'))
