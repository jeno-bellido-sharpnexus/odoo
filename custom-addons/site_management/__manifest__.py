{
    'name': 'Site Management',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Manage sites and their contacts',
    'description': """
        This module allows you to manage sites and their associated contacts.
        Features:
        - Site management
        - Contact management with site relationship
        - REST API endpoints for sites and contacts
    """,
    'depends': ['base', 'web', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/site_views.xml',
        'views/contact_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
