{
    'name': 'Gov Master (政策专家)',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'ChatGPT-powered consultation for registered experts',
    'description': """
Gov Master: 专为注册专家设计的对话平台
- 支持 ChatGPT 对话
- 多格式返回（Markdown, HTML, 图文混排）
""",
    'author': 'Your Name',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/chat_views.xml',
        'views/gov_master_menu.xml',
    ],
    'qweb': [
        'views/chat_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gov_master/static/src/js/chat.js',
            'gov_master/static/src/css/chat.css',
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}