from datetime import date
from app.extensions import db
from app.models import User, Module, Plan, Subscription, FinancialEntry


def seed_everything():
    if User.query.count() == 0:
        admin = User(name='Jeremias Aragão', email='admin@digitalaragao.com', role='admin')
        admin.set_password('123456')
        client = User(name='Cliente Demo', email='cliente@digitalaragao.com', role='client')
        client.set_password('123456')
        db.session.add_all([admin, client])
        db.session.commit()

    if Module.query.count() == 0:
        modules = [
            Module(name='Controle Financeiro', slug='financeiro', category='Financeiro', short_description='Organize entradas, saídas e acompanhe seu caixa em um só lugar.', full_description='Módulo SaaS para controle financeiro com foco em organização, visão de caixa e produtividade.', icon='💰', route_base='/modulos/financeiro', module_mode='internal', is_active=True, is_public=True, is_installed=True, is_saas=True, show_on_home=True, sort_order=1, theme_primary='#42d6ff', theme_secondary='#0f1f35', theme_accent='#8be8ff'),
            Module(name='Portfólio', slug='portfolio', category='Marca', short_description='Apresente projetos, serviços e autoridade profissional.', full_description='Módulo público de portfólio para exibir trabalhos e converter visitantes em contatos.', icon='🖼️', route_base='/modulos/portfolio', module_mode='internal', is_active=True, is_public=True, is_installed=True, is_saas=False, show_on_home=True, sort_order=2, theme_primary='#d4a373', theme_secondary='#2f1b12', theme_accent='#f4d6b6'),
            Module(name='CRM (Clientes)', slug='crm', category='Relacionamento', short_description='Gerencie contatos, clientes e oportunidades.', full_description='Módulo CRM em evolução para acompanhar clientes e oportunidades.', icon='👥', route_base='/modulos/crm', module_mode='internal', is_active=False, is_public=True, is_installed=False, is_saas=True, show_on_home=True, sort_order=3),
        ]
        db.session.add_all(modules)
        db.session.commit()

    financeiro = Module.query.filter_by(slug='financeiro').first()
    if financeiro and Plan.query.count() == 0:
        plans = [
            Plan(name='Financeiro Start', price=29.90, billing_cycle='mensal', description='Plano inicial do módulo financeiro.', module=financeiro),
            Plan(name='Financeiro Pro', price=59.90, billing_cycle='mensal', description='Plano avançado do módulo financeiro.', module=financeiro),
        ]
        db.session.add_all(plans)
        db.session.commit()

    client = User.query.filter_by(email='cliente@digitalaragao.com').first()
    plan = Plan.query.filter_by(name='Financeiro Start').first()
    if client and plan and Subscription.query.count() == 0:
        db.session.add(Subscription(user=client, plan=plan, status='active'))
        db.session.commit()

    if client and FinancialEntry.query.count() == 0:
        entries = [
            FinancialEntry(user=client, description='Assinatura recebida', category='Receita', entry_type='entrada', amount=79.90, reference_date=date.today(), notes='Recebimento demo'),
            FinancialEntry(user=client, description='Hospedagem', category='Despesa', entry_type='saida', amount=25.00, reference_date=date.today(), notes='Custo demo'),
        ]
        db.session.add_all(entries)
        db.session.commit()
