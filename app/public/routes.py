from flask import Blueprint, render_template, request
from app.models import Module, Plan

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def home():
    modules = Module.query.filter_by(show_on_home=True, is_public=True).order_by(Module.sort_order.asc()).all()
    plans = Plan.query.filter_by(is_active=True).order_by(Plan.price.asc()).all()
    return render_template('public/home.html', modules=modules, plans=plans)


@public_bp.route('/solucoes')
def solutions():
    search = request.args.get('q', '').strip()
    query = Module.query.filter_by(is_public=True).order_by(Module.sort_order.asc(), Module.name.asc())
    if search:
        like = f'%{search}%'
        query = query.filter(Module.name.ilike(like) | Module.short_description.ilike(like) | Module.category.ilike(like))
    return render_template('public/solutions.html', modules=query.all(), search=search)


@public_bp.route('/planos')
def plans():
    plans = Plan.query.filter_by(is_active=True).order_by(Plan.price.asc()).all()
    return render_template('public/plans.html', plans=plans)


@public_bp.route('/sobre')
def about():
    return render_template('public/about.html')


@public_bp.route('/contato')
def contact():
    return render_template('public/contact.html')
