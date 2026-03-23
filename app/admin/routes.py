from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import admin_required
from app.services.dashboard_service import admin_metrics
from app.models import Module
from app.extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@admin_required
def dashboard():
    metrics = admin_metrics()
    modules = Module.query.order_by(Module.sort_order.asc(), Module.name.asc()).all()
    return render_template('admin/dashboard.html', metrics=metrics, modules=modules)


@admin_bp.route('/modulos')
@admin_required
def modules():
    modules = Module.query.order_by(Module.sort_order.asc(), Module.name.asc()).all()
    return render_template('admin/modules.html', modules=modules, editing_module=None)


@admin_bp.route('/modulos/novo', methods=['POST'])
@admin_required
def create_module():
    data = _read_module_form()
    if Module.query.filter_by(slug=data['slug']).first():
        flash('Já existe um módulo com esse slug.', 'danger')
        return redirect(url_for('admin.modules'))
    db.session.add(Module(**data))
    db.session.commit()
    flash('Módulo criado com sucesso.', 'success')
    return redirect(url_for('admin.modules'))


@admin_bp.route('/modulos/<int:module_id>/editar', methods=['GET', 'POST'])
@admin_required
def edit_module(module_id):
    module = Module.query.get_or_404(module_id)
    if request.method == 'POST':
        data = _read_module_form()
        for key, value in data.items():
            setattr(module, key, value)
        db.session.commit()
        flash('Módulo atualizado com sucesso.', 'success')
        return redirect(url_for('admin.modules'))
    modules = Module.query.order_by(Module.sort_order.asc(), Module.name.asc()).all()
    return render_template('admin/modules.html', modules=modules, editing_module=module)


@admin_bp.route('/modulos/<int:module_id>/toggle', methods=['POST'])
@admin_required
def toggle_module(module_id):
    module = Module.query.get_or_404(module_id)
    module.is_active = not module.is_active
    db.session.commit()
    flash('Status do módulo atualizado.', 'info')
    return redirect(url_for('admin.modules'))


@admin_bp.route('/modulos/<int:module_id>/delete', methods=['POST'])
@admin_required
def delete_module(module_id):
    module = Module.query.get_or_404(module_id)
    db.session.delete(module)
    db.session.commit()
    flash('Módulo removido com sucesso.', 'info')
    return redirect(url_for('admin.modules'))


def _read_module_form():
    return {
        'name': request.form.get('name', '').strip(),
        'slug': request.form.get('slug', '').strip().lower(),
        'category': request.form.get('category', '').strip(),
        'short_description': request.form.get('short_description', '').strip(),
        'full_description': request.form.get('full_description', '').strip(),
        'icon': request.form.get('icon', '').strip() or '🧩',
        'route_base': request.form.get('route_base', '').strip(),
        'module_mode': request.form.get('module_mode', 'internal').strip(),
        'external_url': request.form.get('external_url', '').strip() or None,
        'sort_order': int(request.form.get('sort_order', '0') or 0),
        'is_public': request.form.get('is_public') == 'on',
        'is_active': request.form.get('is_active') == 'on',
        'is_installed': request.form.get('is_installed') == 'on',
        'is_saas': request.form.get('is_saas') == 'on',
        'show_on_home': request.form.get('show_on_home') == 'on',
        'theme_primary': request.form.get('theme_primary', '').strip() or None,
        'theme_secondary': request.form.get('theme_secondary', '').strip() or None,
        'theme_accent': request.form.get('theme_accent', '').strip() or None,
    }
