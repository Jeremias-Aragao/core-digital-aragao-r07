from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    subscriptions = db.relationship('Subscription', back_populates='user', cascade='all, delete-orphan')
    financial_entries = db.relationship('FinancialEntry', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Module(db.Model):
    __tablename__ = 'modules'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    category = db.Column(db.String(80), nullable=False)
    short_description = db.Column(db.String(255), nullable=False)
    full_description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(20), nullable=True)
    route_base = db.Column(db.String(120), nullable=False)
    module_mode = db.Column(db.String(20), nullable=False, default='internal')
    external_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    is_installed = db.Column(db.Boolean, default=True, nullable=False)
    is_saas = db.Column(db.Boolean, default=False, nullable=False)
    show_on_home = db.Column(db.Boolean, default=True, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    theme_primary = db.Column(db.String(20), nullable=True)
    theme_secondary = db.Column(db.String(20), nullable=True)
    theme_accent = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    plans = db.relationship('Plan', back_populates='module', cascade='all, delete-orphan')

    @property
    def status_label(self) -> str:
        if not self.is_installed:
            return 'não instalado'
        if not self.is_active:
            return 'pausado'
        return 'ativo'


class Plan(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    billing_cycle = db.Column(db.String(20), nullable=False, default='mensal')
    description = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    module = db.relationship('Module', back_populates='plans')
    subscriptions = db.relationship('Subscription', back_populates='plan', cascade='all, delete-orphan')


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='subscriptions')
    plan = db.relationship('Plan', back_populates='subscriptions')


class FinancialEntry(db.Model):
    __tablename__ = 'financial_entries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(180), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    entry_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reference_date = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='financial_entries')
