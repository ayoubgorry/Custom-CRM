{
    'name': 'CRM Avancé',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Fonctionnalités avancées pour la gestion des opportunités',
    'description': """
        Module CRM personnalisé avec:
        - Auto-archivage des opportunités après 30 jours
        - Rappels automatiques par email (7, 15, 30 jours)
        - Système de feedback client via questionnaire
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'crm',
        'mail',
        'survey',
        'base_automation'  # Ajout de la dépendance base_automation
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/automated_actions.xml',
        'data/email_templates.xml',
        'data/survey_data.xml',
        'views/feedback_views.xml',
        'views/settings_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}