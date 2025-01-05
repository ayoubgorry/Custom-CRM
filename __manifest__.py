{
    'name': 'CRM Avancé',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Fonctionnalités avancées pour la gestion des opportunités',
    'description': """
        Module CRM personnalisé avec:
        - Auto-archivage des opportunités après 30 jours
        - Rappels automatiques toutes les 24h
        - Système de feedback client
        - Classification automatique des clients
        - Raisons détaillées de perte d'opportunité
    """,
    'author': 'Bardin lKetaf',
    'website': 'https://github.com/ayoubgorry/Custom-CRM/',
    'depends': [
        'base',
        'crm',
        'mail',
        'survey',
        'base_automation',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizards/lost_reason_views.xml',
        'views/feedback_views.xml',
        'views/settings_views.xml',
        'data/mail_templates.xml',
        'data/cron_jobs.xml',
        'data/automated_actions.xml',
        'data/survey_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}