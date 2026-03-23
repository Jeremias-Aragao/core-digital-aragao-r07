from urllib.parse import quote
from flask import Blueprint, render_template
from app.models import Module

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/modulos/portfolio')


@portfolio_bp.route('/')
def index():
    projetos = [
        {'titulo': 'Portfólio Profissional', 'descricao': 'Página organizada para apresentar serviços, resultados, projetos e autoridade digital.', 'imagem': 'https://via.placeholder.com/900x500?text=Portfolio+1', 'link': '#'},
        {'titulo': 'Landing Page Estratégica', 'descricao': 'Estrutura visual pensada para conversão, credibilidade e apresentação profissional.', 'imagem': 'https://via.placeholder.com/900x500?text=Portfolio+2', 'link': '#'},
        {'titulo': 'Sistema Web Modular', 'descricao': 'Projeto com arquitetura escalável, módulos independentes e base pronta para crescimento.', 'imagem': 'https://via.placeholder.com/900x500?text=Portfolio+3', 'link': '#'},
    ]
    module = Module.query.filter_by(slug='portfolio').first()
    whatsapp_numero = '5581994336238'
    mensagem = 'Olá! Vi o módulo de portfólio no Core Digital Aragão e quero ter meu próprio portfólio.'
    whatsapp_link = f'https://wa.me/{whatsapp_numero}?text={quote(mensagem)}'
    return render_template('modules/portfolio/index.html', projetos=projetos, whatsapp_link=whatsapp_link, module=module)
