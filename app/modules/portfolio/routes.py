from urllib.parse import quote
from flask import Blueprint, render_template

portfolio_bp = Blueprint(
    "portfolio",
    __name__,
    url_prefix="/modulos/portfolio"
)

projects = [
    {
        "title": "Sistema de Pedidos para Lanchonete",
        "problem": "Pedidos manuais causavam lentidão, falhas de comunicação e retrabalho no atendimento.",
        "solution": "Desenvolvimento de um sistema web para cadastro e impressão automática de pedidos na cozinha.",
        "tech": ["Python", "Flask", "HTML", "CSS", "JavaScript"],
        "result": "Mais agilidade no atendimento, menos erros operacionais e melhor organização da operação.",
    },
    {
        "title": "Automação de Envio de Mensagens e PDFs",
        "problem": "O envio manual de documentos e mensagens tomava tempo e prejudicava a rotina operacional.",
        "solution": "Criação de uma automação para agilizar o envio de mensagens e arquivos para clientes.",
        "tech": ["Python", "Automação", "Integrações"],
        "result": "Ganho de produtividade, padronização do processo e economia de tempo.",
    },
    {
        "title": "Automação de Consultas de Processos",
        "problem": "Acompanhamentos manuais em sistemas externos exigiam repetição e aumentavam o risco de erro.",
        "solution": "Desenvolvimento de scripts para coleta e organização de dados de processos.",
        "tech": ["Python", "Excel", "Automação de Processos"],
        "result": "Análises mais rápidas, controle melhorado e tomada de decisão mais eficiente.",
    },
    {
        "title": "Dignidade em Ação",
        "problem": "Projetos sociais costumam enfrentar dificuldades de organização, visibilidade e captação de apoio.",
        "solution": "Planejamento de uma plataforma digital para apoiar voluntariado, doações e gestão de ações sociais.",
        "tech": ["Flask", "UX/UI", "Gestão", "Impacto Social"],
        "result": "Estrutura digital mais clara, potencial de alcance ampliado e maior organização do projeto.",
    },
]

services = [
    {
        "title": "Automação de Processos",
        "description": "Reduzo tarefas manuais e repetitivas para aumentar produtividade e organização.",
        "icon": "⚙️",
    },
    {
        "title": "Desenvolvimento de Sistemas",
        "description": "Crio sistemas web sob medida com foco em rotina, controle e eficiência.",
        "icon": "💻",
    },
    {
        "title": "Integrações",
        "description": "Conecto WhatsApp, Excel, APIs e outras ferramentas ao fluxo do negócio.",
        "icon": "🔗",
    },
    {
        "title": "Organização Empresarial",
        "description": "Estruturo processos e ajudo empresas a trabalharem com mais clareza e resultado.",
        "icon": "📊",
    },
]

skills = [
    "Python",
    "Flask",
    "HTML",
    "CSS",
    "JavaScript",
    "Excel",
    "Automação de Processos",
    "Integração de Sistemas",
    "Gestão Administrativa",
    "UX/UI Estratégico",
]

stats = [
    {"number": "ADM + TI", "label": "Visão combinada de gestão e tecnologia"},
    {"number": "4+", "label": "Frentes de solução aplicáveis a negócios"},
    {"number": "100%", "label": "Foco em resolver problemas reais"},
]


@portfolio_bp.route("/")
def home():
    mensagem = "Olá! Vi o módulo de portfólio no Core Digital Aragão e quero ter meu próprio portfólio."
    whatsapp_link = f"https://wa.me/5581994336238?text={quote(mensagem)}"

    return render_template(
        "modules/portfolio/index.html",
        projects=projects,
        services=services,
        skills=skills,
        stats=stats,
        whatsapp_link=whatsapp_link,
    )
