# -*- coding: utf-8 -*-
{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'A simple library/book management example for Odoo learning',
    'description': 'Demo module to show models, views, security and demo data.',
    'author': 'Hefei Li',
    'category': 'Tools',
    'depends': ['base'],  # 视需要可加入 'contacts' 等
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'data/demo_data.xml',
    ],
    'demo': ['data/demo_data.xml',],
    'installable': True,
    'application': True,
    'auto_install': False,
}
